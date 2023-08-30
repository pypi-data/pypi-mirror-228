#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2022 Ye Chang yech1990@gmail.com
# Distributed under terms of the GNU license.
#
# Created: 2022-07-18 22:42

import sys

import numpy as np
import pandas as pd
import polars as pl
import pyranges as pr


def parse_features(feature_file_name: str) -> pd.DataFrame:
    if feature_file_name.endswith(".bed") or feature_file_name.endswith(
        ".bed.gz"
    ):
        df = pd.read_csv(
            feature_file_name,
            sep="\t",
            names=["Chromosome", "Start", "End", "Name", "Index", "Strand"],
            comment="#",
        )
    else:
        df = pl.read_parquet(feature_file_name).to_pandas()
    df = df.sort_values(["Name", "Index"], ascending=True).assign(
        len_of_window=lambda x: x["End"] - x["Start"]
    )
    df["len_of_feature"] = df.groupby("Name")["len_of_window"].transform("sum")
    df["frac_of_feature"] = (
        df.groupby("Name")["len_of_window"].transform("cumsum")
        - df["len_of_window"]
    ) / df["len_of_feature"]
    df[["Transcript", "Type"]] = df["Name"].str.split(":", expand=True)
    return df


def parse_input(
    input_file_name: str,
    with_header: bool = False,
    col_index: list = [0, 1, 2, 4, 5],
) -> pd.DataFrame:
    if len(col_index) == 5:
        df = pd.read_csv(
            input_file_name,
            sep="\t",
            usecols=col_index,
            names=["Chromosome", "Start", "End", "Score", "Strand"],
            dtype={
                "Chromosome": str,
                "Start": int,
                "End": int,
                "Score": float,
                "Strand": str,
            },
            comment="#",
            skiprows=1 if with_header else 0,
        )
    elif len(col_index) == 4:
        df = pd.read_csv(
            input_file_name,
            sep="\t",
            usecols=col_index,
            names=["Chromosome", "Start", "End", "Strand"],
            dtype={"Chromosome": str, "Start": int, "End": int, "Strand": str},
            comment="#",
            skiprows=1 if with_header else 0,
        ).assign(Score=1.0)
    elif len(col_index) == 3:
        df = pd.read_csv(
            input_file_name,
            sep="\t",
            usecols=col_index,
            names=["Chromosome", "End", "Strand"],
            dtype={"Chromosome": str, "End": int, "Strand": str},
            comment="#",
            skiprows=1 if with_header else 0,
        ).assign(Start=lambda x: x["End"] - 1, Score=1.0)
    df["Chromosome"] = (
        df["Chromosome"].str.replace("chrM", "MT").str.replace("chr", "")
    )
    return df


def annotate_with_feature(
    df_input: pd.DataFrame,
    df_feature: pd.DataFrame,
    nb_cpu=8,
    type_ratios=None,
    bin_number=None,
    annot_name=False,
    keep_all=False,
    by_strand=False,
) -> pd.DataFrame:
    df = (
        pr.PyRanges(df_input)
        .join(
            pr.PyRanges(df_feature),
            suffix="_ref",
            report_overlap=True,
            nb_cpu=nb_cpu,
            strandedness="same" if by_strand else None,
        )
        .df.groupby(
            ["Chromosome", "Start", "End"], as_index=False, group_keys=False
        )
        .apply(lambda x: x.nlargest(1, "Overlap"))
        .assign(
            d=lambda x: np.where(
                x.Strand_ref == "+",
                (np.minimum((x.Start + x.End) // 2, x.End_ref) - x.Start_ref)
                / x.len_of_feature
                + x.frac_of_feature,
                (x.End_ref - np.maximum((x.Start + x.End) // 2, x.Start_ref))
                / x.len_of_feature
                + x.frac_of_feature,
            )
        )
    )

    if type_ratios is not None:
        type_ratios = np.array(type_ratios)
        type2ratio = dict(
            zip(["5UTR", "CDS", "3UTR"], type_ratios / np.sum(type_ratios))
        )
    else:
        # type to ratio is differ for different input bins
        s = (
            df_feature[
                df_feature["Transcript"].isin(df["Transcript"].unique())
            ]
            .groupby(["Transcript", "Type"])["len_of_window"]
            .sum()
            .reset_index()
            .groupby(["Type"])["len_of_window"]
            .median()
        )
        type2ratio = (s / s.sum()).to_dict()
        if (
            "5UTR" not in type2ratio
            or "CDS" not in type2ratio
            or "3UTR" not in type2ratio
        ):
            sys.exit(
                "Error: Given ranges do not overlap all 3 features: "
                "5'UTR, CDS and 3'UTR !"
                "Please use the type_ratios argument instead."
            )
    df["d_norm"] = np.where(
        df["Type"] == "5UTR",
        df["d"] * type2ratio["5UTR"],
        np.where(
            df["Type"] == "CDS",
            df["d"] * type2ratio["CDS"] + type2ratio["5UTR"],
            df["d"] * type2ratio["3UTR"]
            + type2ratio["5UTR"]
            + type2ratio["CDS"],
        ),
    )
    if annot_name:
        df["Name"] = df["Name_ref"]

    if bin_number is not None:
        y, x = np.histogram(
            df["d_norm"], bins=bin_number, weights=df["Score"], range=(0, 1)
        )
        x = (x[1:] + x[:-1]) / 2
        df.attrs.update(
            {
                "bin_number": bin_number,
                "bin_x": list(np.round(x, 6)),
                "bin_y": list(y),
            }
        )

    if not keep_all:
        df = df.loc[
            :, ["Chromosome", "Start", "End", "Name", "d_norm", "Strand"]
        ]
    # Use attrs property to store metadata in dataframe
    # DataFrame.attrs is an experimental feature, use be used with pandas >= 1.0
    df.attrs.update(type2ratio)
    return df


if __name__ == "__main__":
    INPUT_FILE = "../data/input.bed.gz"
    FEATURE_FILE = "../data/features.bed.gz"
    df_feature = parse_features(FEATURE_FILE)
    df_input = parse_input(INPUT_FILE)
    annotate_with_feature(df_input, df_feature).to_csv(
        sys.stdout, sep="\t", index=False, header=False
    )
