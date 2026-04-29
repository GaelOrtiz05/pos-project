#ifndef LOGIN_PASS_HASH_HPP
#define LOGIN_PASS_HASH_HPP
#include <sodium.h>
#include <sodium/crypto_pwhash.h>
#include <string.h>
inline bool hash_password(const char *password,
                          char hashed_output[crypto_pwhash_STRBYTES]) {
  if (sodium_init() < 0) {
    return false;
  }

  return crypto_pwhash_str(hashed_output, password, strlen(password),
                           crypto_pwhash_OPSLIMIT_INTERACTIVE,
                           crypto_pwhash_MEMLIMIT_INTERACTIVE);
}

inline bool check_password(const char *password, const char *stored_hash) {
  if (crypto_pwhash_str_verify(stored_hash, password, strlen(password)) != 0) {
    return false;
  }
  return true;
}

#endif
