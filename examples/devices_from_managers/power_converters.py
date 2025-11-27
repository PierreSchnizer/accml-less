import logging

from accml.custom.facility_specific.bessyii.liasion_translator_setup import (
    load_managers,
)

from accml_less.impl.utils import build_combined_view, add_proxies_to_combined_view

logger = logging.getLogger("accml-mml")


def main():
    yp, lm, ts = load_managers()
    quadrupole_names = yp.get("quadrupoles")
    cv_q = [
        build_combined_view(element_name=name, lm=lm, ts=ts)
        for name in quadrupole_names
    ]
    cvp_q = [add_proxies_to_combined_view(cv) for cv in cv_q]
    # cv.get("design").read("main_strength")
    cv = cv_q[5]
    cvp = cvp_q[5]
    print(cv)
    try:
        cv.get("design").read("main_strengh")
    except NotImplementedError as ne:
        pass

    try:
        cvp.design.main_strength.read
    except NotImplementedError as ne:
        pass
    print(cvp)


if __name__ == "__main__":
    main()
