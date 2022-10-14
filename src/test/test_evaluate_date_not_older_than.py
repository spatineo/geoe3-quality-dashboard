"""Unit tests for date-not-older-than evaluators"""

from datetime import datetime

from ..evaluate import evaluate_results

def test__date_not_older_than__positive():
    """2015-12-15 should be within 6 months of 2016-01-01"""
    test_rule = {
        'evaluationCriteria': {
            'type': 'date-not-older-than',
            'duration': 'P6M'
        }
    }

    test_context = {
        'now': datetime.fromisoformat('2016-01-01')
    }

    result = '2015-12-15'
    
    (value, explanation) = evaluate_results(test_rule['evaluationCriteria'], result, test_context)

    assert value == 1


def test__date_not_older_than__negative():
    """2015-12-15 should be older than 6 months from 2020-01-01"""
    test_rule = {
        'evaluationCriteria': {
            'type': 'date-not-older-than',
            'duration': 'P6M'
        }
    }

    test_context = {
        'now': datetime.fromisoformat('2020-01-01')
    }

    result = '2015-12-15'
    
    (value, explanation) = evaluate_results(test_rule['evaluationCriteria'], result, test_context)

    assert value == 0
    assert explanation == "date 2015-12-15 older than P6M"