/**
 * @fileoverview Terms and Conditions page component with legal terms and BSL license info
 * @module pages/Terms
 */
import React from 'react';

/**
 * Terms and Conditions Page Component
 * 
 * Static legal page outlining the terms and conditions for using Partle,
 * including intellectual property rights, liability limitations, and
 * Business Source License (BSL) information.
 * 
 * Features:
 * - Complete terms and conditions sections
 * - BSL license information with GitHub link
 * - Legal disclaimers and liability limitations
 * - Responsive layout with clear section structure
 * - External link security attributes
 * 
 * @returns JSX element containing the complete terms and conditions
 */
export default function Terms(): JSX.Element {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground p-8">
      <div className="p-8 bg-surface rounded-xl shadow-lg max-w-4xl w-full">
        <h1 className="text-3xl font-bold mb-4 text-center">Terms and Conditions</h1>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">1. Acceptance of Terms</h2>
          <p className="text-base mb-2">
            By accessing and using this website (the "Service"), you accept and agree to be 
            bound by the terms and provisions of this agreement. If you do not agree to abide 
            by the above, please do not use this service.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">2. Use of the Website</h2>
          <p className="text-base mb-2">
            This website and its components are offered for informational purposes only; this 
            site shall not be responsible or liable for the accuracy, usefulness or availability 
            of any information transmitted or made available via the site, and shall not be 
            responsible or liable for any error or omissions in that information.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">3. Intellectual Property</h2>
          <p className="text-base mb-2">
            The content, organization, graphics, design, compilation, and other matters related 
            to the Website are protected under applicable copyrights, trademarks, and other 
            proprietary (including but not limited to intellectual property) rights. The copying, 
            redistribution, use, or publication by you of any such matters or any part of the 
            Website is strictly prohibited.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">4. Limitation of Liability</h2>
          <p className="text-base mb-2">
            The website and its content are provided "as is" without any warranties of any kind, 
            either express or implied, including but not limited to warranties of merchantability, 
            fitness for a particular purpose, or non-infringement. In no event shall the website 
            owner be liable for any damages whatsoever, including direct, indirect, incidental, 
            consequential, special, or punitive damages, arising out of or in connection with 
            your use of the website.
          </p>
        </section>

        <section className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">5. BSL License Information</h2>
          <p className="text-base mb-2">
            The source code for this project is licensed under the Business Source License (BSL). 
            You can find the full text of the BSL license in the{' '}
            <a 
              href="https://github.com/rubenayla/partle/blob/main/LICENSE" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-blue-500 hover:underline"
            >
              LICENSE
            </a>
            {' '}file in the project's GitHub repository. This license permits free use, 
            modification, and distribution under certain conditions, typically related to 
            commercial use and the passage of time, after which the code may revert to an 
            open-source license like Apache 2.0.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">6. Changes to Terms</h2>
          <p className="text-base mb-2">
            We reserve the right to change these conditions from time to time as we see fit 
            and your continued use of the site will signify your acceptance of any adjustment 
            to these terms. Any changes to our privacy policy will be posted on our website 
            30 days prior to these changes taking place.
          </p>
        </section>
      </div>
    </div>
  );
}
