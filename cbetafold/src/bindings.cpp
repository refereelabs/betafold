#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>

#include "training/Trainer.h"
#include "exceptions/BetafoldError.h"


namespace py = pybind11;


PYBIND11_MODULE(betafold, m) {
  py::class_<Trainer>(m, "Trainer")
      .def(py::init<>())
      .def("train", &Trainer::train);

  py::register_local_exception<BetafoldError>(m, "BetafoldError", PyExc_RuntimeError);

  m.doc() = "A C++ python library for fast AI physics simulations";
}