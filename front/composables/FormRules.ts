export const FormRules: Record<string, ((value: any) => string | boolean)[]> = {
  notEmpty: [(v: string | null) => !!v || 'This field is required'],
}
