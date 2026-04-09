from app.services.analysis.graphs.lecture_pre_graph import build_lecture_pre_graph
from app.services.analysis.graphs.lecture_agg_graph import build_lecture_agg_graph


class AnalysisGraphFactory:
    def __init__(self):
        self._graphs = {
            "lecture_pre": build_lecture_pre_graph(),
            "lecture_agg": build_lecture_agg_graph(),
        }

    def get_graph(self, name: str):
        graph = self._graphs.get(name)
        if graph is None:
            raise ValueError(f"Graph not found: {name}")
        return graph


analysis_graph_factory = AnalysisGraphFactory()