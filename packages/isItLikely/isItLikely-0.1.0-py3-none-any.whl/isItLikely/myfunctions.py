def probability(event_occurrences, total_outcomes):
    """
    Calculates the probability of an event.

    Parameters:
    event_occurrences (int): The number of favorable outcomes.
    total_outcomes (int): The total number of possible outcomes.

    Returns:
    float: The probability of the event occurring.
    """
    return event_occurrences / total_outcomes

def complementary_probability(event_occurrences, total_outcomes):
    """
    Calculates the complementary probability (probability of "not" an event).

    Parameters:
    event_occurrences (int): The number of unfavorable outcomes.
    total_outcomes (int): The total number of possible outcomes.

    Returns:
    float: The probability of the event not occurring.
    """
    return 1 - probability(event_occurrences, total_outcomes)

def joint_probability(probability_event1, probability_event2, *args):
    """
    Calculates the joint probability of two or more independent events occurring.

    Parameters:
    probability_event1, probability_event2, ... (float): Probabilities of individual events.

    Returns:
    float: The joint probability of all events occurring.
    """
    joint_prob = 1
    for prob in (probability_event1, probability_event2, *args):
        joint_prob *= prob
    return joint_prob

def conditional_probability(probability_event_given_condition, probability_condition):
    """
    Calculates the conditional probability of an event given a condition.

    Parameters:
    probability_event_given_condition (float): Probability of the event given the condition.
    probability_condition (float): Probability of the condition.

    Returns:
    float: The conditional probability of the event given the condition.
    """
    return probability_event_given_condition / probability_condition

def addition_rule_disjoint(probability_event1, probability_event2, *args):
    """
    Calculates the probability of the union of two or more disjoint events.

    Parameters:
    probability_event1, probability_event2, ... (float): Probabilities of individual events.

    Returns:
    float: The probability of the union of all disjoint events.
    """
    return sum([probability_event1, probability_event2, *args])

def addition_rule_non_disjoint(probability_event1, probability_event2, *args, probability_intersection):
    """
    Calculates the probability of the union of two or more non-disjoint events using the inclusion-exclusion principle.

    Parameters:
    probability_event1, probability_event2, ... (float): Probabilities of individual events.
    probability_intersection (float): Probability of the intersection of all events.

    Returns:
    float: The probability of the union of all non-disjoint events.
    """
    return sum([probability_event1, probability_event2, *args]) - probability_intersection


