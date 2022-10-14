"""Evaluation functions that are used to evaluate results extracted from the model"""

from datetime import datetime
import isodate

def evaluate_date_not_older_than(eval_criteria, result, context):
    # result is expected to be in ISO format
    result_as_date = datetime.fromisoformat(result)

    duration = isodate.parse_duration(eval_criteria['duration'])
    reference = context['now'] - duration
    if result_as_date < reference:
        value = (0, f"date {result} older than {eval_criteria['duration']}")
    else:
        value = (1, f"date {result} not older than {eval_criteria['duration']}") 
    
    return value

evaluator_by_type = {
    'date-not-older-than': evaluate_date_not_older_than
}

def evaluate_results(eval_criteria, result, context):
    evaluator = evaluator_by_type[eval_criteria['type']]

    if evaluator is None:
        raise f"unknown evaluation method {eval_criteria['type']}"

    return evaluator(eval_criteria, result, context)
