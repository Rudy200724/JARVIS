import { useState } from "react";
import { LockKeyhole, User, Eye, EyeOff, LogIn } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL;

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!username.trim() || !password) {
      setError("Please enter your username and password.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",

        credentials: "include",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          username: username.trim(),
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Invalid username or password."
        );
      }

      onLogin();

    } catch (error) {
      setError(
        error.message || "Unable to connect to JARVIS."
      );

    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="login-page">

      <div className="login-glow login-glow-one" />
      <div className="login-glow login-glow-two" />

      <div className="login-grid" />

      <div className="login-container">

        <div className="login-brand">

          <div className="login-core">
            <div className="login-core-inner" />
          </div>

          <h1>J.A.R.V.I.S</h1>

          <p>
            JUST A RATHER VERY INTELLIGENT SYSTEM
          </p>

        </div>


        <form
          className="login-card"
          onSubmit={handleSubmit}
        >

          <div className="login-card-header">

            <div className="login-status">
              <span className="login-status-dot" />
              SYSTEM SECURE
            </div>

            <h2>Welcome back</h2>

            <p>
              Authenticate to access your JARVIS core.
            </p>

          </div>


          <div className="login-field">

            <label htmlFor="username">
              USERNAME
            </label>

            <div className="login-input-wrapper">

              <User size={18} />

              <input
                id="username"
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(event) =>
                  setUsername(event.target.value)
                }
                autoComplete="username"
                disabled={loading}
              />

            </div>

          </div>


          <div className="login-field">

            <label htmlFor="password">
              PASSWORD
            </label>

            <div className="login-input-wrapper">

              <LockKeyhole size={18} />

              <input
                id="password"
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Enter password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                autoComplete="current-password"
                disabled={loading}
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
                tabIndex="-1"
              >
                {showPassword ? (
                  <EyeOff size={18} />
                ) : (
                  <Eye size={18} />
                )}
              </button>

            </div>

          </div>


          {error && (
            <div className="login-error">
              {error}
            </div>
          )}


          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="login-spinner" />
                AUTHENTICATING...
              </>
            ) : (
              <>
                <LogIn size={18} />
                ACCESS JARVIS
              </>
            )}

          </button>


          <div className="login-footer">

            <span className="login-footer-line" />

            <span>
              AUTHORIZED ACCESS ONLY
            </span>

            <span className="login-footer-line" />

          </div>

        </form>

      </div>

    </div>
  );
}

export default Login;