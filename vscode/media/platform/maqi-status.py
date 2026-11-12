"""The MaQI status bar for VS Code: what JupyterLab's MaQI bar shows (memory,
data rights, idle countdown, egress), computed by MaQI's own code - maqi_lab's
server extension and quota, maqi_data's health check - never re-implemented.

Run by the extension with the hub's Python on a MaQI machine:
    /opt/tljh/user/bin/python maqi-status.py [fr|en]
Prints {"items": [{"id", "text", "tooltip", "level"}]}: no secret, ever (the
key files are read only to hand them to maqi_data, as the hub does).
"""
import datetime as dt
import json
import os
import pwd
import sys
import time

FR = (sys.argv[1:] or ["en"])[0] == "fr"
USER = pwd.getpwuid(os.getuid()).pw_name
KEYS = "/run/maqi/keys/%s" % USER
# Under the extension's XDG state folder, never in ~/.maqi (the platform's).
CACHE = os.path.join(os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state"), "maqi", "status-cache.json")
WASABI_TTL = 300          # the probe lists every bucket (~4 s); rights change rarely


def say(fr, en):
    return fr if FR else en


def env_file(name):
    vals = {}
    try:
        with open(os.path.join(KEYS, name), encoding="utf-8") as f:
            for line in f:
                line = line.strip().removeprefix("export ")
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    vals[k] = v.strip().strip("'\"")
    except OSError:
        pass
    return vals


def gb(n):
    return ("%.1f Go" if FR else "%.1f GB") % (n / 2**30)


def until(iso):
    try:
        left = dt.datetime.fromisoformat(iso.replace("Z", "+00:00")) - dt.datetime.now(dt.timezone.utc)
    except ValueError:
        return ""
    m = int(left.total_seconds() // 60)
    return say("expiré", "expired") if m <= 0 else ("%d h %02d" % (m // 60, m % 60) if m >= 60 else "%d min" % m)


def session_cgroup():
    """The session JupyterLab measures: the person's Jupyter server unit, where
    its kernels and the browser VS Code run. A process started over SSH lives
    elsewhere (its own scope), so the unit is read by name, then our own."""
    unit = "/sys/fs/cgroup/system.slice/jupyter-%s.service" % USER
    if os.path.exists(os.path.join(unit, "memory.current")):
        return unit
    with open("/proc/self/cgroup", encoding="utf-8") as f:
        rel = next(l.split("::", 1)[1].strip() for l in f if l.startswith("0::"))
    return "/sys/fs/cgroup" + rel


def read(base, name):
    with open(os.path.join(base, name), encoding="utf-8") as f:
        return f.read().strip()


def limit(base, name):
    v = read(base, name)
    return None if v == "max" else int(v)


def memory(base, connected):
    """As maqi_lab.serverext._memory: the working set (current minus inactive
    file cache) against the session's limits."""
    stat = dict(l.split() for l in read(base, "memory.stat").splitlines() if " " in l)
    events = dict(l.split() for l in read(base, "memory.events").splitlines() if " " in l)
    used = max(0, int(read(base, "memory.current")) - int(stat.get("inactive_file", 0)))
    soft, hard, core = limit(base, "memory.high"), limit(base, "memory.max"), limit(base, "memory.low")
    killed, slowed = int(events.get("oom_kill", 0)), int(events.get("high", 0))
    cap = soft or hard
    level = "error" if killed else "warn" if cap and used > 0.9 * cap else "ok"
    tip = [say("Mémoire de votre session (noyaux, VS Code), comme la barre JupyterLab.",
               "Your session's memory (kernels, VS Code), as JupyterLab's bar.")]
    if core: tip.append(say("Part garantie : ", "Guaranteed share: ") + gb(core))
    if soft: tip.append(say("Ralentie au-delà de ", "Slowed above ") + gb(soft))
    if hard: tip.append(say("Un noyau est arrêté à ", "A kernel is stopped at ") + gb(hard))
    if connected: tip.append(say("Sessions sur la machine : %d", "Sessions on the machine: %d") % connected)
    if slowed: tip.append(say("Ralentie %d fois", "Slowed %d times") % slowed)
    if killed: tip.append(say("Noyaux arrêtés : %d", "Kernels stopped: %d") % killed)
    return {"id": "memory", "text": "RAM %s%s" % (gb(used), " / " + gb(cap) if cap else ""),
            "tooltip": "\n".join(tip), "level": level}


def cpu(base):
    """The session's CPU over one second, against its share (cpu.max)."""
    def usage():
        return int(dict(l.split() for l in read(base, "cpu.stat").splitlines())["usage_usec"])
    q = read(base, "cpu.max").split()
    cores = int(q[0]) / int(q[1]) if q[0] != "max" else os.cpu_count()
    u0, t0 = usage(), time.monotonic()
    time.sleep(1)
    used = (usage() - u0) / 1e6 / (time.monotonic() - t0)
    pct = 100 * used / cores
    return {"id": "cpu", "text": "CPU %d %%" % round(pct),
            "tooltip": say("Processeur de votre session : %.1f cœur(s) utilisés sur %g alloués (machine : %d).",
                           "Your session's CPU: %.1f core(s) in use of %g allotted (machine: %d).") % (used, cores, os.cpu_count()),
            "level": "warn" if pct > 90 else "ok"}


def wasabi():
    try:
        with open(CACHE, encoding="utf-8") as f:
            c = json.load(f)
        if time.time() - c.get("at", 0) < WASABI_TTL:
            return c["value"]
    except (OSError, ValueError, KeyError):
        pass
    os.environ.update(env_file("wasabi.env"))
    try:
        from maqi_data import health
        r = health.check()
        value = {"state": r.get("state"), "message": r.get("message"), "datasets": r.get("datasets", 0),
                 "buckets": [{"bucket": b.get("bucket"), "ok": bool(b.get("ok"))} for b in r.get("buckets", [])]}
    except Exception as e:  # a broken probe must not break the bar
        value = {"state": "down", "message": ("%s: %s" % (type(e).__name__, e))[:160], "datasets": 0, "buckets": []}
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump({"at": time.time(), "value": value}, f)
    except OSError:
        pass
    return value


def data_item():
    w = wasabi()
    ok = [b["bucket"] for b in w["buckets"] if b["ok"]]
    denied = [b["bucket"] for b in w["buckets"] if not b["ok"]]
    expire = env_file("wasabi.env").get("MAQI_WASABI_EXPIRE", "")
    left = until(expire) if expire else ""
    tip = ["Wasabi : %s" % (w.get("message") or w.get("state"))]
    tip += ["✓ " + b for b in ok] + ["✗ " + b for b in denied]
    if left: tip.append(say("Identifiants renouvelés dans ", "Credentials renewed in ") + left)
    level = "ok" if w.get("state") == "ok" else "warn" if ok else "error"
    text = "$(database) %d/%d · %d %s" % (len(ok), len(w["buckets"]), w.get("datasets", 0), say("jeux", "datasets"))
    return {"id": "data", "text": text, "tooltip": "\n".join(tip), "level": level}


def idle_item(serverext):
    """The machine's idle verdict (the fleet's idle cron, every ten minutes)."""
    d = serverext._idle()
    if not d or not d.get("status"):
        return None
    why = d.get("why") or []
    why = why if isinstance(why, list) else [str(why)]
    busy = d["status"] == "busy"
    text = "$(pulse) " + (say("active", "active") if busy else say("inactive", "idle"))
    tip = (say("La machine reste allumée : ", "The machine stays on: ") if busy
           else say("Inactive : elle s'éteindra après %d min sans activité.", "Idle: it stops after %d min without activity.") % d.get("delay_minutes", 0))
    return {"id": "idle", "text": text, "tooltip": tip + ("\n" + "\n".join(why) if why else ""),
            "level": "ok" if busy else "warn"}


def egress_item(quota):
    try:
        st = quota.status("egress_gb")
    except Exception:
        return None
    if not st.get("live"):
        return None
    return {"id": "egress", "text": "$(cloud-upload) %s" % st.get("used_str", ""),
            "tooltip": say("Données sorties de la machine (compteur MaQI) : %s sur %s.",
                           "Data sent out of the machine (MaQI meter): %s of %s.") % (st.get("used_str"), st.get("limit_str")),
            "level": "error" if st.get("over") else "warn" if st.get("warn") else "ok"}


def main():
    items = []
    try:
        from maqi_lab import quota, serverext
    except Exception:
        quota = serverext = None
    try:
        base = session_cgroup()
    except Exception:
        base = None
    connected = serverext._connected() if serverext else None
    for make in ((lambda: memory(base, connected)) if base else None, (lambda: cpu(base)) if base else None, data_item,
                 (lambda: idle_item(serverext)) if serverext else None, (lambda: egress_item(quota)) if quota else None):
        if make is None:
            continue
        try:
            it = make()
        except Exception:
            it = None
        if it:
            items.append(it)
    print(json.dumps({"items": items}, ensure_ascii=False))


main()
