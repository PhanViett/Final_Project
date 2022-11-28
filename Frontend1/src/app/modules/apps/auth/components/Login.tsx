/* eslint-disable jsx-a11y/anchor-is-valid */
import clsx from "clsx";
import { useFormik } from "formik";
import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import * as Yup from "yup";
import { useAuth } from "../core/Auth";
import { getUserByToken, login } from "../core/_requests";

const loginSchema = Yup.object().shape({
  email: Yup.string().min(3, "Minimum 1 symbols").max(50, "Maximum 50 symbols"),
  password: Yup.string()
    .min(3, "Minimum 1 symbols")
    .max(50, "Maximum 50 symbols")
    .required("Password is required"),
});

const initialValues = {
  email: "chuyenvien",
  password: "123456abcA",
};

/*
  Formik+YUP+Typescript:
  https://jaredpalmer.com/formik/docs/tutorial#getfieldprops
  https://medium.com/@maurice.de.beijer/yup-validation-and-typescript-and-formik-6c342578a20e
*/

export function Login() {
  const [loading, setLoading] = useState(false);
  // const { saveAuth, setCurrentUser, setRoleUser } = useAuth();

  const formik = useFormik({
    initialValues,
    validationSchema: loginSchema,
    onSubmit: async (values, { setStatus, setSubmitting }) => {
      setLoading(true);
      try {
        const { data: auth } = await login(values.email, values.password);
        console.log("log auth : " + auth);
        // saveAuth(auth);
        const { data: user } = await getUserByToken(auth.access_token);
        // setCurrentUser(user);
        // setRoleUser(user?.assigned_role);
      } catch (error: any) {
        // saveAuth(undefined);
        setStatus("The login detail is incorrect");
        setSubmitting(false);
        setLoading(false);
        toast.error(error?.response?.data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      }
    },
  });

  return (
    <form
      className="form w-100"
      onSubmit={formik.handleSubmit}
      noValidate
      id="kt_login_signin_form"
    >
      {/* begin::Heading */}
      <div className="text-center mb-10">
        <h1 className="text-dark mb-3">Sign In to Metronic</h1>
        <div className="text-gray-400 fw-bold fs-4">
          New Here?{" "}
          <Link to="/auth/registration" className="link-primary fw-bolder">
            Create an Account
          </Link>
        </div>
      </div>
      {/* begin::Heading */}

      {/* begin::Form group */}
      <div className="fv-row mb-10">
        <label className="form-label fs-6 fw-bolder text-dark">Email</label>
        <input
          placeholder="Email"
          {...formik.getFieldProps("email")}
          className={clsx(
            "form-control form-control-lg form-control-solid",
            {
              "is-invalid": formik.touched.email && formik.errors.email,
            },
            {
              "is-valid": formik.touched.email && !formik.errors.email,
            }
          )}
          type="email"
          name="email"
          autoComplete="off"
        />
        {formik.touched.email && formik.errors.email && (
          <div className="fv-plugins-message-container">
            <span role="alert">{formik.errors.email}</span>
          </div>
        )}
      </div>
      {/* end::Form group */}

      {/* begin::Form group */}
      <div className="fv-row mb-10">
        <div className="d-flex justify-content-between mt-n5">
          <div className="d-flex flex-stack mb-2">
            {/* begin::Label */}
            <label className="form-label fw-bolder text-dark fs-6 mb-0">
              Password
            </label>
            {/* end::Label */}
            {/* begin::Link */}
            <Link
              to="/forgot-password"
              className="link-primary fs-6 fw-bolder"
              style={{ marginLeft: "5px" }}
            >
              Forgot Password ?
            </Link>
            {/* end::Link */}
          </div>
        </div>
        <input
          type="password"
          autoComplete="off"
          {...formik.getFieldProps("password")}
          className={clsx(
            "form-control form-control-lg form-control-solid",
            {
              "is-invalid": formik.touched.password && formik.errors.password,
            },
            {
              "is-valid": formik.touched.password && !formik.errors.password,
            }
          )}
        />
        {formik.touched.password && formik.errors.password && (
          <div className="fv-plugins-message-container">
            <div className="fv-help-block">
              <span role="alert">{formik.errors.password}</span>
            </div>
          </div>
        )}
      </div>
      {/* end::Form group */}

      {/* begin::Action */}
      <div className="text-center">
        <button
          type="submit"
          id="kt_sign_in_submit"
          className="btn btn-lg btn-primary w-100 mb-5"
          disabled={formik.isSubmitting || !formik.isValid}
        >
          {!loading && <span className="indicator-label">Continue</span>}
          {loading && (
            <span className="indicator-progress" style={{ display: "block" }}>
              Please wait...
              <span className="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          )}
        </button>
      </div>
      {/* end::Action */}
    </form>
  );
}
