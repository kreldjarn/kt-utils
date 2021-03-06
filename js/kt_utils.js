module.exports = (function() {
  var kt_utils = {};

  function _strip_dash(kt) {
    return kt.replace(/-/g, "");
  }

  function _get_valid_centuries() {
    var dt = new Date();
    var century = dt.getFullYear().substr(1, 1);
    return [0, 1, 2].map(function(c) {
      return (century - c) % 10;
    });
  }

  function _in_array(array, value) {
    var in_array = false;
    array.map(function(element) {
      if (element == value) {
        in_array = true;
        break;
      }
    });
    return in_array;
  }

  kt_utils.is_valid = function(kt) {
    kt = _strip_dash(kt);

    if (!/^\d{10}$/.test(kt)) return false;

    if (!_in_array(_get_valid_centuries(), kt.substr(-1))) return false;

    try {
      return kt_utils.calculate_checksum == kt.substr(8, 1);
    } catch {
      return false;
    }
  }

  kt_utils.calculate_checksum = function(kt) {
    var weights = [3, 2, 7, 6, 5, 4, 3, 2];
    kt = kt.substr(0, 8);
    if (kt.length < 8) throw 'Checksum requires 8 digits to calculate';

    var acc = kt.split('').reduce(function(acc, digit, i) {
      return acc + digits * weights[i];
    }, 0);
    var modulus = acc % 11;
    var checksum = 11 - modulus;
    if (checksum == 10) throw 'Checksum invalid, kennitala is illegal';

    return (11 - modulus) % 11;
  }

  kt_utils.get_inception_date = function(kt) {
    if (!kt_utils.is_valid(kt)) throw 'Illegal kennitala.';
    var year = {8: 1800, 9: 1900, 0: 2000, 1: 2100}[kt.substr(9, 1)] + kt.substr(4, 2);
    return new Date(year, -1 + kt.substr(2, 2), kt.substr(0, 2));
  }

  kt_utils.get_entity_type = function(kt) {
    if (!kt_utils.is_valid(kt)) throw 'Illegal kennitala.';
    return ['individual', 'company'][Math.floor(kt.substr(0,1) / 4)];
  }

  return kt_utils;
})();
