
from numpy.testing import assert_equal

from benchmarks.test_benchmarks import build_lawrence_instance
from pyjobshop import Model, ProblemData


def test_json():
    """
    Tests whether serialization and deserialization of a given instance
    leaves the ProblemData (and solver result) unaffected.

    Solving is useful because the ProblemData instances may be subtly
    different (e.g. using a list vs a tuple) without affecting the solution.
    Therefore, we check the solver result first, and only then instance
    equality.
    """
    model_orig: Model = build_lawrence_instance()
    result_orig = model_orig.solve(display=False)

    # Create the original model data
    pd_orig: ProblemData = model_orig.data()
    json_str = pd_orig.to_json(indent=2)
    # json.dumps(pd_orig, cls=JSONDataclassEncoder, indent=2)

    with open("test-output.json", "w") as f:
        f.write(json_str + "\n")

    pd_new: ProblemData = ProblemData.from_json(json_str)
    # pd_new: ProblemData = json.loads(json_str, cls=ProblemDataDecoder)
    model_new = Model.from_data(pd_new)
    result_new = model_new.solve(display=False)

    assert_equal(result_orig.objective, result_new.objective)
    assert_equal(pd_orig, pd_new)
