// Validaciones de perfil (cliente) - sin dependencias externas
// Nota: estas validaciones son "puras" y pueden reutilizarse en cualquier componente.

/**
 * Extrae solo dígitos.
 * @param {string|number|null|undefined} value
 * @returns {string}
 */
export function onlyDigits(value) {
  return String(value ?? '').replace(/\D+/g, '');
}

/**
 * Valida cédula ecuatoriana (10 dígitos) usando algoritmo Módulo 10.
 * Reglas:
 * - Longitud 10
 * - Provincia: 01-24
 * - Tercer dígito: 0-5 (persona natural)
 * - Dígito verificador (último) coincide con cálculo.
 *
 * @param {string|number|null|undefined} cedula
 * @returns {{ isValid: boolean, error: string }}
 */
export function validateEcuadorCedula(cedula) {
  const digits = onlyDigits(cedula);

  if (!digits) return { isValid: false, error: 'La cédula es requerida.' };
  if (digits.length !== 10) return { isValid: false, error: 'La cédula debe tener 10 dígitos.' };

  const province = Number(digits.slice(0, 2));
  if (Number.isNaN(province) || province < 1 || province > 24) {
    return { isValid: false, error: 'Provincia inválida en la cédula.' };
  }

  const third = Number(digits[2]);
  if (Number.isNaN(third) || third > 5) {
    return { isValid: false, error: 'Cédula inválida (tercer dígito).' };
  }

  const checkDigit = Number(digits[9]);
  if (Number.isNaN(checkDigit)) {
    return { isValid: false, error: 'Cédula inválida.' };
  }

  // Módulo 10: coeficientes 2,1,2,1,2,1,2,1,2 en las 9 primeras posiciones
  let sum = 0;
  for (let i = 0; i < 9; i += 1) {
    const n = Number(digits[i]);
    if (Number.isNaN(n)) return { isValid: false, error: 'Cédula inválida.' };
    const coef = i % 2 === 0 ? 2 : 1;
    let p = n * coef;
    if (p >= 10) p -= 9;
    sum += p;
  }

  const computed = (10 - (sum % 10)) % 10;
  if (computed !== checkDigit) {
    return { isValid: false, error: 'Cédula inválida (dígito verificador).' };
  }

  return { isValid: true, error: '' };
}

/**
 * Teléfono: solo dígitos y longitud exacta de 10.
 * @param {string|number|null|undefined} phone
 * @returns {{ isValid: boolean, error: string }}
 */
export function validatePhone10(phone) {
  const digits = onlyDigits(phone);
  if (!digits) return { isValid: false, error: 'El teléfono es requerido.' };
  if (digits.length !== 10) return { isValid: false, error: 'El teléfono debe tener 10 dígitos.' };
  return { isValid: true, error: '' };
}

/**
 * Email: regex estándar.
 * @param {string|null|undefined} email
 * @returns {{ isValid: boolean, error: string }}
 */
export function validateEmail(email) {
  const value = String(email ?? '').trim();
  if (!value) return { isValid: false, error: 'El email es requerido.' };

  // Regex "estándar" (práctico) para correo
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!re.test(value)) return { isValid: false, error: 'Email inválido.' };

  return { isValid: true, error: '' };
}

/**
 * Valida un campo de perfil según su key.
 * @param {string} key
 * @param {any} value
 * @returns {string} error message (vacío si no hay error o si no aplica)
 */
export function getProfileFieldError(key, value) {
  if (key === 'cedula') return validateEcuadorCedula(value).error;
  if (key === 'telefono') return validatePhone10(value).error;
  if (key === 'email') return validateEmail(value).error;
  return '';
}


