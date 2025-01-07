import type { FieldValidationMetaInfo } from '@constructor/ui';
import { generateErrorMessage } from '@constructor/ui';

/**
 * Get from https://github.com/logaretm/vee-validate/blob/main/packages/i18n/src/utils.ts
 * Example: The {field} value must be between 0:{min} and 1:{max}
 */
export function generateMessage(context: FieldValidationMetaInfo<unknown>) {
  return generateErrorMessage(context, {}, {});
}
