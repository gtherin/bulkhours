// The agent's Markdown in the panel: what students see, and what can never
// get through (any tag the agent writes is shown as text).
import { test } from "node:test";
import assert from "node:assert/strict";
import "../media/markdown.js";

const { markdown } = (globalThis as any).bhMarkdown as { markdown(s: string): string };

test("headings become headings, a step smaller in a narrow panel", () => {
  assert.equal(markdown("## Where your sessions live\nAll here:"), "<h4>Where your sessions live</h4><p>All here:</p>");
  assert.equal(markdown("# Title"), "<h3>Title</h3>");
});

test("bullet and numbered lists, nested by indentation", () => {
  assert.equal(markdown("- one\n- two\n  - two.a\n- three"),
    "<ul><li>one</li><li>two<ul><li>two.a</li></ul></li><li>three</li></ul>");
  assert.equal(markdown("1. first\n2. second"), "<ol><li>first</li><li>second</li></ol>");
  assert.equal(markdown("3. third\n4. fourth"), '<ol start="3"><li>third</li><li>fourth</li></ol>');
});

test("a table with its header", () => {
  assert.equal(markdown("| model | price |\n|---|---|\n| fast | $0.30 |"),
    '<div class="table"><table><thead><tr><th>model</th><th>price</th></tr></thead><tbody><tr><td>fast</td><td>$0.30</td></tr></tbody></table></div>');
});

test("quotes, rules, and a paragraph that keeps its line breaks", () => {
  assert.equal(markdown("> careful\n> here"), "<blockquote><p>careful<br>here</p></blockquote>");
  assert.equal(markdown("a\n\n---\n\nb"), "<p>a</p><hr><p>b</p>");
  assert.equal(markdown("line one\nline two"), "<p>line one<br>line two</p>");
});

test("inline: bold, italic, strike, code, and links only to safe schemes", () => {
  assert.equal(markdown("**bold** *it* _it_ ~~gone~~ `a*b*c`"),
    "<p><strong>bold</strong> <em>it</em> <em>it</em> <del>gone</del> <code>a*b*c</code></p>");
  assert.equal(markdown("[doc](https://x.fr) [bad](javascript:alert)"), '<p><a href="https://x.fr">doc</a> bad</p>');
  assert.equal(markdown("snake_case_name stays"), "<p>snake_case_name stays</p>");
});

test("code blocks are shown verbatim, Markdown inside them included", () => {
  assert.equal(markdown("```cuda\n__global__ void k() {} // **not bold**\n```"),
    "<pre><code>__global__ void k() {} // **not bold**\n</code></pre>");
});

test("whatever the agent writes, no tag of its own gets through", () => {
  const html = markdown('<img src=x onerror=alert(1)>\n## <script>x</script>\n- <b>no</b>\n| <i>a</i> |\n|---|\n| b |');
  assert.ok(!/<(img|script|b|i)[\s>]/.test(html), html);
  assert.match(html, /&lt;script&gt;/);
});
