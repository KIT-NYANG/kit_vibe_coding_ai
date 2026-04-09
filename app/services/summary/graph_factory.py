# services/summary/graph_factory.py - 그래프들을 등록해두는 곳

from app.services.summary.graphs.lecture_summary_graph import build_lecture_summary_graph


class GraphFactory:
    def __init__(self):
        self._graphs = {
            "lecture_summary": build_lecture_summary_graph(),
        }

    def get_graph(self, name: str):
        graph = self._graphs.get(name)
        if graph is None:
            raise ValueError(f"Graph not found: {name}")
        return graph


graph_factory = GraphFactory()