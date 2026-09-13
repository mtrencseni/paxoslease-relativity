# PaxosLease with Moving Participants

A short note on running PaxosLease when the participants are in relativistic
relative motion. Companion to
[PaxosLease Revisited](https://github.com/mtrencseni/paxoslease-revisited-2026).

The safety property of PaxosLease says that at any time at most one proposer
holds the lease. "At any time" assumes the participants agree on which events
happen together, which fails once they move with respect to one another. The
note restates the property so it does not depend on a choice of frame, and
shows what the protocol costs once it is restated: the structure is unchanged,
and two timing rules each acquire one factor of the relativistic Doppler factor
`k = sqrt((1+beta)/(1-beta))`.

## Build

    make pdf        # paper/PaxosLease-Relativity.pdf
    make figures    # regenerate the spacetime diagrams from figures/figs.py
    make clean

`make pdf` needs `latexmk` and a TeX Live with `elsarticle`. `make figures`
needs Python with `matplotlib`, and is only required if the diagrams change;
the built PDFs are checked in.

## Layout

    paper/      the note
    figures/    figs.py, and the three spacetime diagrams it generates
