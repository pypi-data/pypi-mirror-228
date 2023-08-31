#!/usr/bin/env python3
import argparse
import typing as t
from pathlib import Path

from astropy import units as u

import artistools as at


def addargs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-scalefactor", "-s", default=0.5, help="Kinetic energy scale factor")
    parser.add_argument("-inputpath", "-i", default=".", help="Path of input files")
    parser.add_argument("-outputpath", "-o", default=".", help="Path of output files")


def eval_mshell(dfmodel, t_model_init_seconds):
    dfmodel = dfmodel.eval(
        "cellmass_grams = 10 ** logrho * 4. / 3. * @math.pi * (velocity_outer ** 3 - velocity_inner ** 3)"
        "* (1e5 * @t_model_init_seconds) ** 3",
    )


def main(args: argparse.Namespace | None = None, argsraw: t.Sequence[str] | None = None, **kwargs) -> None:
    if args is None:
        parser = argparse.ArgumentParser(
            formatter_class=at.CustomArgHelpFormatter,
            description="Fully mix an ARTIS model to homogenous composition and save back to ARTIS format.",
        )

        addargs(parser)
        parser.set_defaults(**kwargs)
        args = parser.parse_args(argsraw)

    dfmodel, t_model_init_days, _ = at.inputmodel.get_modeldata_tuple(args.inputpath)
    print("Read model.txt")
    dfelabundances = at.inputmodel.get_initelemabundances(args.inputpath)
    print("Read abundances.txt")

    t_model_init_seconds = t_model_init_days * 24 * 60 * 60

    eval_mshell(dfmodel, t_model_init_seconds)

    print(dfmodel)
    print(dfelabundances)

    model_mass_grams = dfmodel.cellmass_grams.sum()
    print(f"model mass: {model_mass_grams * u.g.to('solMass'):.3f} Msun")
    for column_name in [x for x in dfmodel.columns if x.startswith("X_")]:
        integrated_mass_grams = (dfmodel[column_name] * dfmodel.cellmass_grams).sum()
        global_massfrac = integrated_mass_grams / model_mass_grams
        print(f"{column_name:>13s}: {global_massfrac:.3f}  ({integrated_mass_grams * u.g.to('solMass'):.3f} Msun)")
        dfmodel = dfmodel.eval(f"{column_name} = {global_massfrac}")

    for column_name in [x for x in dfelabundances.columns if x.startswith("X_")]:
        integrated_mass_grams = (dfelabundances[column_name] * dfmodel.cellmass_grams).sum()
        global_massfrac = integrated_mass_grams / model_mass_grams
        print(f"{column_name:>13s}: {global_massfrac:.3f}  ({integrated_mass_grams * u.g.to('solMass'):.3f} Msun)")
        dfelabundances = dfelabundances.eval(f"{column_name} = {global_massfrac}")

    print(dfmodel)
    print(dfelabundances)

    modeloutfilename = "model_fullymixed.txt"
    at.save_modeldata(
        dfmodel=dfmodel, t_model_init_days=t_model_init_days, filename=Path(args.outputpath, modeloutfilename)
    )
    print(f"Saved {modeloutfilename}")

    abundoutfilename = "abundances_fullymixed.txt"
    at.inputmodel.save_initelemabundances(dfelabundances, Path(args.outputpath, abundoutfilename))
    print(f"Saved {abundoutfilename}")


if __name__ == "__main__":
    main()
