import logging

from flask_restx import Namespace, Resource

from bookbnb_middleware.api.handlers.metrics_handlers import get_all_metrics
from bookbnb_middleware.api.models.metrics_models import (
    metric_datum_model,
    metric_model,
    metrics_parser,
    error_model,
)

log = logging.getLogger(__name__)

ns = Namespace(
    name="Metrics",
    path="/bookbnb/metrics",
    description="Operations related to bookbnb metrics",
)

ns.models[metric_model.name] = metric_model
ns.models[metric_datum_model.name] = metric_datum_model
ns.models[error_model.name] = error_model


@ns.route("")
class MetricsResource(Resource):
    @ns.expect(metrics_parser)
    @ns.response(code=400, description="Unexpected error")
    @ns.marshal_list_with(metric_model)
    def get(self):
        """
        Get all metrics.
        """
        res, status_code = get_all_metrics(metrics_parser.parse_args())
        return res, status_code
