// Validaciones de tarjeta (cliente) - simulación estructural (sin pasarelas reales)

/**
 * @param {string|number|null|undefined} value
 * @returns {string}
 */
export function onlyDigits(value) {
  return String(value ?? '').replace(/\D+/g, '');
}

/**
 * Luhn algorithm.
 * @param {string} digits - solo números
 * @returns {boolean}
 */
export function isValidLuhn(digits) {
  if (!digits || /[^0-9]/.test(digits)) return false;

  let sum = 0;
  let shouldDouble = false;
  for (let i = digits.length - 1; i >= 0; i -= 1) {
    let n = Number(digits[i]);
    if (Number.isNaN(n)) return false;
    if (shouldDouble) {
      n *= 2;
      if (n > 9) n -= 9;
    }
    sum += n;
    shouldDouble = !shouldDouble;
  }
  return sum % 10 === 0;
}

/**
 * Detecta marca por BIN (prefijos) + longitudes típicas.
 * @param {string|number|null|undefined} cardNumber
 * @returns {{ code: string, label: string } | null}
 */
export function detectCardBrand(cardNumber) {
  const digits = onlyDigits(cardNumber);
  if (!digits) return null;

  const prefix1 = digits.slice(0, 1);
  const prefix2 = digits.slice(0, 2);
  const prefix3 = digits.slice(0, 3);
  const prefix4 = digits.slice(0, 4);
  const prefix6 = digits.slice(0, 6);

  const p2 = Number(prefix2);
  const p3 = Number(prefix3);
  const p4 = Number(prefix4);
  const p6 = Number(prefix6);

  // Visa: 4...
  if (prefix1 === '4') return { code: 'visa', label: 'Visa' };

  // Amex: 34, 37
  if (prefix2 === '34' || prefix2 === '37') return { code: 'amex', label: 'American Express' };

  // MasterCard: 51-55 y 2221-2720
  if ((p2 >= 51 && p2 <= 55) || (p4 >= 2221 && p4 <= 2720)) {
    return { code: 'mastercard', label: 'MasterCard' };
  }

  // Discover: 6011, 65, 644-649, 622126-622925
  if (
    prefix4 === '6011' ||
    prefix2 === '65' ||
    (p3 >= 644 && p3 <= 649) ||
    (p6 >= 622126 && p6 <= 622925)
  ) {
    return { code: 'discover', label: 'Discover' };
  }

  // Diners Club: 300-305, 36, 38-39
  if ((p3 >= 300 && p3 <= 305) || prefix2 === '36' || (p2 >= 38 && p2 <= 39)) {
    return { code: 'diners', label: 'Diners Club' };
  }

  // JCB: 3528-3589
  if (p4 >= 3528 && p4 <= 3589) return { code: 'jcb', label: 'JCB' };

  // UnionPay (muy general): 62...
  if (prefix2 === '62') return { code: 'unionpay', label: 'UnionPay' };

  return { code: 'unknown', label: 'Tarjeta' };
}

/**
 * Normaliza expiry a MM/AA (solo dígitos + '/')
 * @param {string|null|undefined} value
 * @returns {string}
 */
export function formatExpiry(value) {
  const digits = onlyDigits(value).slice(0, 4);
  if (digits.length <= 2) return digits;
  return `${digits.slice(0, 2)}/${digits.slice(2)}`;
}

/**
 * Valida fecha de vencimiento MM/AA (no menor al mes/año actual).
 * @param {string|null|undefined} expiry
 * @param {Date} [now]
 * @returns {{ isValid: boolean, error: string }}
 */
export function validateExpiry(expiry, now = new Date()) {
  const value = String(expiry ?? '').trim();
  if (!value) return { isValid: false, error: 'La fecha de vencimiento es requerida.' };

  const match = value.match(/^(\d{2})\s*\/\s*(\d{2})$/);
  if (!match) return { isValid: false, error: 'Formato inválido. Usa MM/AA.' };

  const month = Number(match[1]);
  const year2 = Number(match[2]);
  if (Number.isNaN(month) || month < 1 || month > 12) {
    return { isValid: false, error: 'Mes inválido.' };
  }

  // Interpretación 20YY (suficiente para esta validación estructural)
  const year = 2000 + year2;
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth() + 1;

  if (year < currentYear || (year === currentYear && month < currentMonth)) {
    return { isValid: false, error: 'La tarjeta está vencida.' };
  }

  return { isValid: true, error: '' };
}

/**
 * Valida CVV (3 dígitos general, 4 dígitos Amex).
 * @param {string|number|null|undefined} cvv
 * @param {{ code: string } | null} brand
 * @returns {{ isValid: boolean, error: string }}
 */
export function validateCvv(cvv, brand) {
  const digits = onlyDigits(cvv);
  if (!digits) return { isValid: false, error: 'El CVV es requerido.' };

  const isAmex = brand?.code === 'amex';
  const requiredLen = isAmex ? 4 : 3;

  if (digits.length !== requiredLen) {
    return { isValid: false, error: `El CVV debe tener ${requiredLen} dígitos.` };
  }
  return { isValid: true, error: '' };
}

/**
 * Valida nombre del titular: solo letras y espacios, mínimo 2 palabras.
 * Soporta acentos/ñ.
 * @param {string|null|undefined} holderName
 * @returns {{ isValid: boolean, error: string }}
 */
export function validateHolderName(holderName) {
  const value = String(holderName ?? '').trim().replace(/\s+/g, ' ');
  if (!value) return { isValid: false, error: 'El nombre del titular es requerido.' };

  // Al menos 2 palabras, solo letras (incluye acentos) y espacios
  const re = /^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:\s+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)+$/;
  if (!re.test(value)) return { isValid: false, error: 'Ingresa nombre y apellido (solo letras).' };

  return { isValid: true, error: '' };
}

/**
 * Valida número de tarjeta por longitud y Luhn.
 * @param {string|number|null|undefined} cardNumber
 * @returns {{ isValid: boolean, error: string, brand: { code: string, label: string } | null }}
 */
export function validateCardNumber(cardNumber) {
  const digits = onlyDigits(cardNumber);
  if (!digits) return { isValid: false, error: 'El número de tarjeta es requerido.', brand: null };

  const brand = detectCardBrand(digits);

  // Longitudes típicas por marca (validación estructural)
  const len = digits.length;
  const allowedLengthsByBrand = {
    visa: [13, 16, 19],
    mastercard: [16],
    amex: [15],
    discover: [16, 19],
    diners: [14],
    jcb: [16, 17, 18, 19],
    unionpay: [16, 17, 18, 19],
    unknown: [12, 13, 14, 15, 16, 17, 18, 19]
  };
  const allowed = allowedLengthsByBrand[brand?.code || 'unknown'] || allowedLengthsByBrand.unknown;

  if (!allowed.includes(len)) {
    return { isValid: false, error: 'Longitud de tarjeta inválida.', brand };
  }

  if (!isValidLuhn(digits)) {
    return { isValid: false, error: 'Número de tarjeta inválido', brand };
  }

  return { isValid: true, error: '', brand };
}

/**
 * Valida toda la tarjeta y devuelve errores por campo.
 * @param {{ number?: any, expiry?: any, cvv?: any, holderName?: any }} cardInfo
 * @param {Date} [now]
 * @returns {{ isValid: boolean, brand: { code: string, label: string } | null, errors: { number?: string, expiry?: string, cvv?: string, holderName?: string } }}
 */
export function validateCardInfo(cardInfo, now = new Date()) {
  const numberRes = validateCardNumber(cardInfo?.number);
  const expiryRes = validateExpiry(cardInfo?.expiry, now);
  const holderRes = validateHolderName(cardInfo?.holderName);
  const cvvRes = validateCvv(cardInfo?.cvv, numberRes.brand);

  const errors = {};
  if (!numberRes.isValid) errors.number = numberRes.error;
  if (!expiryRes.isValid) errors.expiry = expiryRes.error;
  if (!cvvRes.isValid) errors.cvv = cvvRes.error;
  if (!holderRes.isValid) errors.holderName = holderRes.error;

  return {
    isValid: Object.keys(errors).length === 0,
    brand: numberRes.brand,
    errors
  };
}


