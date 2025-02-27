//
// Created by andrew on 2/27/25.
//

#ifndef BETAFOLD_CBETAFOLD_INCLUDE_EXCEPTIONS_BETAFOLDERROR_H_
#define BETAFOLD_CBETAFOLD_INCLUDE_EXCEPTIONS_BETAFOLDERROR_H_

#include <exception>
#include <string>
#include <stdexcept>

class BetafoldError : public std::exception {
 public:
  explicit BetafoldError(const char *m) : message{m} {}
  explicit BetafoldError(std::string &m) : message{m} {}
  [[nodiscard]] auto what() const noexcept -> const char * override { return message.c_str(); }
 private:
  std::string message;

};

#endif //BETAFOLD_CBETAFOLD_INCLUDE_EXCEPTIONS_BETAFOLDERROR_H_
