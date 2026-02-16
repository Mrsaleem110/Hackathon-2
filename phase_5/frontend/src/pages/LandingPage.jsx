import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LandingPage = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="landing-page">
      <div className="landing-container">
        <header className="landing-header">
          <h1>Welcome to Todo AI Chatbot</h1>
          <p>Your intelligent task management assistant</p>
        </header>

        <main className="landing-main">
          <section className="features-section">
            <h2>Features</h2>
            <div className="features-grid">
              <div className="feature-card">
                <h3>📝 Smart Task Management</h3>
                <p>Create, track, and manage your tasks with AI assistance.</p>
              </div>
              <div className="feature-card">
                <h3>🤖 AI-Powered Chatbot</h3>
                <p>Interact with our intelligent assistant to manage your tasks.</p>
              </div>
              <div className="feature-card">
                <h3>📊 Analytics & Insights</h3>
                <p>Track your productivity with detailed analytics.</p>
              </div>
            </div>
          </section>

          <section className="cta-section">
            {!isAuthenticated ? (
              <>
                <h2>Get Started Today</h2>
                <p>Join thousands of users who are already boosting their productivity.</p>
                <div className="auth-buttons">
                  <Link to="/register" className="btn btn-primary">
                    Sign Up Free
                  </Link>
                  <Link to="/login" className="btn btn-secondary">
                    Sign In
                  </Link>
                </div>
              </>
            ) : (
              <>
                <h2>Welcome Back!</h2>
                <p>You're already signed in. Access your dashboard to get started.</p>
                <Link to="/dashboard" className="btn btn-primary">
                  Go to Dashboard
                </Link>
              </>
            )}
          </section>
        </main>

        <footer className="landing-footer">
          <p>© 2024 Todo AI Chatbot. All rights reserved.</p>
        </footer>
      </div>

      <style jsx>{`
        .landing-page {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }

        .landing-container {
          max-width: 1200px;
          width: 100%;
          background: white;
          border-radius: 10px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
          overflow: hidden;
        }

        .landing-header {
          text-align: center;
          padding: 60px 40px 40px;
          background: #f8f9fa;
        }

        .landing-header h1 {
          font-size: 2.5rem;
          color: #333;
          margin-bottom: 10px;
        }

        .landing-header p {
          font-size: 1.2rem;
          color: #666;
          margin: 0;
        }

        .landing-main {
          padding: 40px;
        }

        .features-section h2,
        .cta-section h2 {
          text-align: center;
          color: #333;
          margin-bottom: 30px;
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
          margin-bottom: 40px;
        }

        .feature-card {
          background: #f8f9fa;
          padding: 30px;
          border-radius: 8px;
          text-align: center;
          transition: transform 0.2s ease;
        }

        .feature-card:hover {
          transform: translateY(-5px);
        }

        .feature-card h3 {
          color: #333;
          margin-bottom: 15px;
        }

        .feature-card p {
          color: #666;
          line-height: 1.6;
        }

        .cta-section {
          text-align: center;
          padding: 40px;
          background: #f0f4f8;
          border-radius: 8px;
        }

        .auth-buttons {
          display: flex;
          gap: 15px;
          justify-content: center;
          margin-top: 20px;
          flex-wrap: wrap;
        }

        .btn {
          padding: 12px 30px;
          border: none;
          border-radius: 6px;
          text-decoration: none;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-primary {
          background: #667eea;
          color: white;
        }

        .btn-primary:hover {
          background: #5a6fd8;
          transform: translateY(-2px);
        }

        .btn-secondary {
          background: #6c757d;
          color: white;
        }

        .btn-secondary:hover {
          background: #5a6268;
          transform: translateY(-2px);
        }

        .landing-footer {
          text-align: center;
          padding: 20px;
          background: #f8f9fa;
          color: #666;
          border-top: 1px solid #dee2e6;
        }

        @media (max-width: 768px) {
          .landing-header {
            padding: 40px 20px 20px;
          }

          .landing-header h1 {
            font-size: 2rem;
          }

          .landing-main {
            padding: 20px;
          }

          .auth-buttons {
            flex-direction: column;
            align-items: center;
          }

          .btn {
            width: 200px;
          }
        }
      `}</style>
    </div>
  );
};

export default LandingPage;