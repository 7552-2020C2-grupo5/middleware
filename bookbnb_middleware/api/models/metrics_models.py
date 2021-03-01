from flask_restx import Model, fields, reqparse

metrics_parser = reqparse.RequestParser()
metrics_parser.add_argument("start_date", type=str, help="initial date", required=True)
metrics_parser.add_argument("end_date", type=str, help="final date", required=True)

metric_datum_model = Model(
    "Metric datum",
    {
        "date": fields.Date(required=True, description="The date of the datum"),
        "value": fields.Float(required=True, description="The value of the datum"),
    },
)

metric_model = Model(
    "Metric",
    {
        "name": fields.String(),
        "data": fields.List(fields.Nested(metric_datum_model, description="The data")),
    },
)

error_model = Model(
    "Metrics error model",
    {"message": fields.String(description="A message describing the error")},
)
