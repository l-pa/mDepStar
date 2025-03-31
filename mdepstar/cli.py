import argparse
from mdepstar import mDepStar, Network

parser = argparse.ArgumentParser(
    prog="mDepStar", description="Mutually Dependent Star method", epilog="Help"
)

parser.add_argument("filename", help="PPI network")
parser.add_argument(
    "-d",
    "--dependency",
    type=float,
    help="Set dependency threshold, if not set estimated value is used",
)
parser.add_argument(
    "-D",
    "--delimiter",
    default=";",
    help="Network file column delimiter - nodeA delimiter nodeB delimiter weight",
)
parser.add_argument("-o", "--output", help="Export predicted complexes")
parser.add_argument(
    "-m", "--mdepexport", action="store_true", help="Export mDep network"
)
parser.add_argument("-w", "--weighted", action="store_true", help="Weighted network")
parser.add_argument("-n", "--node", help="Specific protein node")
parser.add_argument("-s", "--skip", action="store_true", help="Skip calculation of statistics")
parser.add_argument("-l", "--local", action="store_true", help="Local version")



args = parser.parse_args()


def main():
    print("v2")
    G: Network = Network()
    G.read_file(args.filename, args.delimiter, args.weighted)
    
    if not args.skip:
        print(f"<k> {G.avg_degree}, <CC> {G.clustering_coeficient()}")
        print("{} nodes / {} edges".format(len(G.nodes()), len(G.edges())))
    
    mdep_star = mDepStar(G)
    res = None
    if not args.local:
        if not args.dependency:
            print(f"Estimated dependency -> {mdep_star.dependency_threshold}")
        else:
            mdep_star.dependency_threshold = float(args.dependency)

        res = mdep_star.get_complexes(args.node)
    else:
        res = mdep_star.get_complexes_local(args.node)

    if args.mdepexport:
        mdep_star.export_mDep_network(
            "{}_mDep.csv".format(args.filename.split("\\")[-1].split("_")[0])
        )

    if args.output:
        print(
            "Found {} complexes, file name {}".format(
                len(res), args.output + "_clusters.txt"
            )
        )
        mdep_star.export(res, args.output + "_clusters.txt")

    else:
        print("Found {} complexes, no output (use -o)".format(len(res)))


if __name__ == "__main__":
    main()
