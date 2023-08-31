from enum import Enum
import json

class Goal(Enum):
    """An enumeration representing the different types of goals a Criteria can have."""

    NONE = 0
    MAXIMIZE = 1
    MINIMIZE = 2
    TARGET = 3
    IN_RANGE = 4
    EQUAL_TO = 5
    CPK = 6

    def __str__(self):
        return self.name


class Optimizer:
    """The Optimizer class is used to set criteria on one or more Analyses,
    then use those criteria to find the optimal parameters.
    """

    def __init__(self, client):
        self._client = client

        result = self._client.send_payload({
            "method": "GET",
            "uri": "optimizer",
        })

        self._criteria = []
        self._solutions = tuple()

    def __str__(self):
        out = ''
        for c in self._criteria:
            if c.goal != Goal.NONE:
                out += '{}\n'.format(c)
        out += "Found {} solutions:".format(len(self._solutions))
        for s in self._solutions:
            out += '{}\n'.format(s)
        return out

    def have_criteria(self):
        for c in self._criteria:
            if c._factor and c.goal == Goal.NONE:
                return False
        return True

    def add_criteria(self, criteria):
        if criteria._factor and criteria.goal==Goal.NONE:
            raise ValueError("Can't add criteria - no goal specified for '{}'.".format(criteria.name))
        if criteria.restrict_discrete==True:
            if not criteria._factor:
                raise ValueError("Can't add criteria - It is not a discrete factor. For response/analysis '{}', restrict_discrete must be False.".format(criteria.name))
            if (criteria._factor.type!="Numeric") or (criteria._factor.type=="Numeric" and criteria._factor.subtype!="Discrete"):
                raise ValueError("Can't add criteria - It is not a discrete factor. For factor '{}', restrict_discrete must be False.".format(criteria.name))
        self._criteria.append(criteria)

    @property
    def solutions(self):
        return self._solutions

    def optimize(self):
        """ Runs the optimization routine. Must have one or more Criteria specified. """

        if not self.have_criteria():
            raise ValueError("Can't run optimization - no criteria specified!")

        result = self._client.send_payload({
            "method": "POST",
            "uri": "optimizer",
            "criteria": [ c.to_json() for c in self._criteria ],
        })
        solutions = []
        for solution in result['payload']['solutions']:
            solutions.append(json.loads(solution))
        self._solutions = tuple(solutions)


class Criteria:
    """The Criteria class is used by the optimizer to calculate a desirability score
    for a given point in the design space, which is then used to search for an optimal point.

    Each Analysis and Factor can have a Criteria (e.g. you might maximize the output of an Analysis,
    and target a certain value of a Factor).
    """

    def __init__(self, factor=None, analysis=None):
        """ Create a Criteria for a Factor or Analysis. """

        if (not analysis and not factor) or (analysis and factor):
            raise ValueError("You must pass in either an analysis or factor.")

        self._analysis = analysis
        self._factor = factor

        self._name = ''
        self._goal = Goal.NONE
        self._target = 0
        self._lower_limit = 0
        self._upper_limit = 0
        self._lower_weight = 1
        self._upper_weight = 1
        self._importance = 3
        self._restrict_discrete = False

    def __str__(self):
        name = ''
        if self._analysis:
            name += self._analysis.name
        if self._factor:
            name += self._factor.name
        return "Criteria for {} -> Goal: {} Target: {} Lower Limit: {} Upper Limit: {} Lower Weight: {} Upper Weight: {} Importance: {} Restrict discrete: {}".format(
            name,
            self._goal,
            self._target,
            self._lower_limit,
            self. _upper_limit,
            self._lower_weight,
            self._upper_weight,
            self._importance,
            self._restrict_discrete,
        )
        if self._factor:
            result += " " + "Restrict discrete: "+ str(self._restrict_discrete)
        return result

    @property
    def name(self):
        """ The name of this Criteria (analysis/response or factor name). """
        if self._analysis:
            self._name = self._analysis.name
        elif self._factor:
            self._name = self._factor.name
        else:
            raise ValueError("You must pass in either an analysis or factor.")
        return self._name

    @property
    def goal(self):
        """ The goal of this Criteria (e.g. Goal.MAXIMIZE). """
        return self._goal

    @goal.setter
    def goal(self, goal):
        self._goal = goal

    @property
    def target(self):
        """ The target for this Criteria, if using Goal.EQUAL_TO or Goal.TARGET """
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def lower_limit(self):
        """ The lower limit for this Criteria. """
        return self._lower_limit

    @lower_limit.setter
    def lower_limit(self, lower_limit):
        self._lower_limit = lower_limit

    @property
    def upper_limit(self):
        """ The upper limit for this Criteria. """
        return self._upper_limit

    @upper_limit.setter
    def upper_limit(self, upper_limit):
        self._upper_limit = upper_limit

    @property
    def lower_weight(self):
        """ The lower weight for this Criteria. """
        return self._lower_weight

    @lower_weight.setter
    def lower_weight(self, lower_weight):
        self._lower_weight = lower_weight

    @property
    def upper_weight(self):
        """ The upper weight for this Criteria. """
        return self._upper_weight

    @upper_weight.setter
    def upper_weight(self, upper_weight):
        self._upper_weight = upper_weight

    @property
    def importance(self):
        """ The importance of this Criteria, relative to other Criteria. """
        return self._importance

    @importance.setter
    def importance(self, importance):
        self._importance = importance

    @property
    def restrict_discrete(self):
        """ The restrict discrete for this Criteria. """
        return self._restrict_discrete

    @restrict_discrete.setter
    def restrict_discrete(self, restrict_discrete):
        self._restrict_discrete = restrict_discrete

    def to_json(self):
        out_dict = {
            'analysis': self._analysis.name if self._analysis else None,
            'factor': self._factor.name if self._factor else None,
            'goal': str(self._goal),
        }

        # the rest of the members are primitives
        for k, v in self.__dict__.items():
            key = k[1:] # strip off leading underscore
            if key in out_dict.keys():
                continue
            out_dict[key] = v
        return out_dict

