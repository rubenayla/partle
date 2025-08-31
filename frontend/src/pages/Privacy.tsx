/**
 * @fileoverview Privacy Policy page component with GDPR compliance information
 * @module pages/Privacy
 */
import React from 'react';

/**
 * Privacy Policy Page Component
 * 
 * Static legal page outlining Partle's privacy practices, data collection,
 * usage policies, and user rights under GDPR. Essential for legal compliance
 * and user transparency.
 * 
 * Features:
 * - Comprehensive privacy policy sections
 * - GDPR compliance information
 * - User data rights explanation
 * - Contact information for privacy inquiries
 * - Responsive layout with clear section structure
 * 
 * @returns JSX element containing the complete privacy policy
 */
export default function Privacy(): JSX.Element {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground p-8">
      <div className="p-8 bg-surface rounded-xl shadow-lg max-w-4xl w-full">
        <h1 className="text-3xl font-bold mb-4 text-center">Privacy Policy</h1>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">1. Introduction</h2>
          <p className="text-base mb-2">
            Welcome to Partle. We are committed to protecting your privacy. This Privacy Policy 
            explains how we collect, use, disclose, and safeguard your information when you visit 
            our website.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">2. Information We Collect</h2>
          <p className="text-base mb-2">
            We may collect information that you provide directly to us, such as when you create 
            an account, add products or stores, or contact us. This may include your name, email 
            address, and any other information you choose to provide.
          </p>
          <p className="text-base mb-2">
            We may also collect certain information automatically when you visit our website, 
            such as your IP address, browser type, operating system, referring URLs, and 
            information about your interactions with the site.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">3. How We Use Your Information</h2>
          <p className="text-base mb-2">
            We use the information we collect to:
          </p>
          <ul className="list-disc list-inside ml-4 mb-2">
            <li>Provide, operate, and maintain our website;</li>
            <li>Improve, personalize, and expand our website;</li>
            <li>Understand and analyze how you use our website;</li>
            <li>Develop new products, services, features, and functionality;</li>
            <li>
              Communicate with you, either directly or through one of our partners, including 
              for customer service, to provide you with updates and other information relating 
              to the website, and for marketing and promotional purposes;
            </li>
            <li>Process your transactions; and</li>
            <li>Find and prevent fraud.</li>
          </ul>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">4. Data Sharing and Disclosure</h2>
          <p className="text-base mb-2">
            We do not sell, trade, or otherwise transfer to outside parties your personally 
            identifiable information unless we provide users with advance notice. This does not 
            include website hosting partners and other parties who assist us in operating our 
            website, conducting our business, or serving our users, so long as those parties 
            agree to keep this information confidential. We may also release information when 
            its release is appropriate to comply with the law, enforce our site policies, or 
            protect ours or others' rights, property or safety.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">5. Data Security</h2>
          <p className="text-base mb-2">
            We implement a variety of security measures to maintain the safety of your personal 
            information when you enter, submit, or access your personal information.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">
            6. Your Data Protection Rights Under GDPR (General Data Protection Regulation)
          </h2>
          <p className="text-base mb-2">
            If you are a resident of the European Economic Area (EEA), you have certain data 
            protection rights. We aim to take reasonable steps to allow you to correct, amend, 
            delete, or limit the use of your Personal Data.
          </p>
          <p className="text-base mb-2">
            If you wish to be informed what Personal Data we hold about you and if you want it 
            to be removed from our systems, please contact us.
          </p>
          <p className="text-base mb-2">
            In certain circumstances, you have the following data protection rights:
          </p>
          <ul className="list-disc list-inside ml-4 mb-2">
            <li>The right to access, update or to delete the information we have on you.</li>
            <li>The right of rectification.</li>
            <li>The right to object.</li>
            <li>The right of restriction.</li>
            <li>The right to data portability.</li>
            <li>The right to withdraw consent.</li>
          </ul>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">7. Changes to This Privacy Policy</h2>
          <p className="text-base mb-2">
            We may update our Privacy Policy from time to time. We will notify you of any 
            changes by posting the new Privacy Policy on this page.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">8. Contact Us</h2>
          <p className="text-base mb-2">
            If you have any questions about this Privacy Policy, please contact us at 
            ruben.jimenezmejias@gmail.com.
          </p>
        </section>
      </div>
    </div>
  );
}
