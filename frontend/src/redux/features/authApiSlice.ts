import { AnyUser, CompanyRegister } from "@/types/auth";
import { apiSlice } from "../api";

const authApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getUser: builder.query<AnyUser, void>({
      query: () => "/auth/user",
    }),
    registerCompany: builder.mutation({
      query: (newCompany: CompanyRegister) => ({
        url: "/companies/create",
        method: "POST",
        body: newCompany,
      }),
    }),
    login: builder.mutation({
      query: ({ email, password }) => ({
        url: "/auth/token/create",
        method: "POST",
        body: { email, password },
      }),
    }),
    /**
     * To be used in a hook on intial page load to check if the user is logged in.
     **/
    verify: builder.mutation({
      query: () => ({
        url: "/auth/token/verify/",
        method: "POST",
      }),
    }),
    logout: builder.mutation({
      query: () => ({
        url: "/auth/logout/",
        method: "POST",
      }),
    }),
  }),
});

export const {
  useGetUserQuery,
  useRegisterCompanyMutation,
  useLoginMutation,
  useVerifyMutation,
  useLogoutMutation,
} = authApiSlice;
