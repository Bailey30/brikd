export interface AuthUser {
  id: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  type: string;
}

export interface Company extends AuthUser {
  organsation: string;
}

export interface User extends AuthUser {
  employmentStatus: string;
}

export interface CompanyRegister {
  email: string;
  password: string;
  organisation: string;
}

export interface UserRegister {
  email: string;
  password: string;
}

export type AnyUser = Company | User;
