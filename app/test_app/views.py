import uuid

from flask import Blueprint, request, current_app
from werkzeug.local import LocalProxy

from app.extension import db
from app.test_app.models import TestModel
from app.test_app.schemas import TestModelSchema
from app.helpers.response_helpers import success_response, error_response
from app.messages.test_app_msg import TEST_MSG

# Create a blueprint for the logger service
test_app = Blueprint('test_app', __name__)
logger = LocalProxy(lambda: current_app.logger)


@test_app.route('/test-route', methods=['GET'])
def test_route():
    logger.info('app test route hit')
    return success_response(
        {}, "Successfully run test-route", 200
    )


@test_app.route('/add/test_model', methods=['POST'])
def add_test_model():
    data = request.get_json()

    # Validate and deserialize input using the schema
    test_model_schema = TestModelSchema()
    errors = test_model_schema.validate(data)
    if errors:
        return error_response(msg='Validation failed', data=errors)

    # Create a new TestModel instance
    try:
        new_test_model = TestModel(**data, test_model=str(uuid.uuid4()))
        db.session.add(new_test_model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error creating TestModel: {e}')
        return error_response(msg='Error creating TestModel', data={'error': str(e)})

    # Serialize and return the created instance
    result = test_model_schema.dump(new_test_model)
    return success_response(data=result, msg=TEST_MSG.get('test_model_created'))
