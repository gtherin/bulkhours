import pandas as pd
import bulkhours


def test_engraving_scale():
    scales = bulkhours.get_data("hpc.engraving_scale")


def test_transistor_count():
    scales = bulkhours.get_data("hpc.transistor_count")


def test_FLOPS_units():
    scales = bulkhours.get_data("hpc.FLOPS_units")


def test_FLOPS_gpus():
    scales = bulkhours.get_data("hpc.FLOPS_gpus")


def test_FLOPS_cpus():
    scales = bulkhours.get_data("hpc.FLOPS_cpus")
