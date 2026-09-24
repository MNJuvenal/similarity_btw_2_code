import argparse

from pdg_parser import load_pdgs_by_src
from graph import match_pair


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compute PDG similarities between source files.'
    )
    parser.add_argument(
        'input_dir', nargs='?', default='test2',
        help='directory containing source files (default: test2)'
    )
    parser.add_argument(
        'output_file', nargs='?', default='similarities.txt',
        help='file receiving similarity results (default: similarities.txt)'
    )
    args = parser.parse_args()

    pdgs_by_src = {
        source_path: [
            graph for graph in graphs
            if len(graph.edges) > 10 or len(graph.nodes) > 10
        ]
        for source_path, graphs in load_pdgs_by_src(args.input_dir).items()
    }
    source_paths = sorted(pdgs_by_src)

    with open(args.output_file, 'w', encoding='utf-8') as output:
        for index, source_1 in enumerate(source_paths):
            for source_2 in source_paths[index + 1:]:
                best_match = None
                for graph_1 in pdgs_by_src[source_1]:
                    for graph_2 in pdgs_by_src[source_2]:
                        distance = match_pair(graph_1, graph_2)
                        if distance is not None:
                            best_match = (
                                distance if best_match is None
                                else min(best_match, distance)
                            )

                result = f"Similarity {source_1} <-> {source_2}: {best_match}\n"
                output.write(result)
                print(result, end='')

