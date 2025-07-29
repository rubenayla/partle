
import React from 'react';

const About = () => {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-foreground mb-6">What is Partle?</h1>
        
        <div className="space-y-6 text-lg text-foreground">
          <p>
            Have you ever spent a whole day driving to multiple stores, searching for a specific, hard-to-find item like a special screw or a unique craft supply, only to come home empty-handed? Partle was created to solve this exact problem.
          </p>
          
          <p>
            <span className="font-semibold">Partle is a search engine for physical stores.</span> It connects you with local businesses, allowing you to check their inventory from the comfort of your home. Our goal is to bridge the gap between the convenience of online shopping and the immediate availability of local stores.
          </p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 pt-8 text-left">
        <div>
          <h2 className="text-2xl font-semibold text-primary mb-3 text-center">For Shoppers</h2>
          <ul className="list-disc list-inside space-y-2">
            <li><span className="font-semibold">Save Time:</span> Find what you need without the guesswork.</li>
            <li><span className="font-semibold">Discover Local:</span> Easily locate items in stores near you.</li>
            <li><span className="font-semibold">Support Community:</span> Help local businesses thrive.</li>
          </ul>
        </div>
        <div>
          <h2 className="text-2xl font-semibold text-primary mb-3 text-center">For Store Owners</h2>
          <ul className="list-disc list-inside space-y-2">
            <li><span className="font-semibold">Increase Visibility:</span> Showcase your products to a wider audience.</li>
            <li><span className="font-semibold">Drive Foot Traffic:</span> Attract customers who are ready to buy.</li>
            <li><span className="font-semibold">Sell Your Way:</span> An alternative to big e-commerce platforms.</li>
          </ul>
        </div>
      </div>

      <div className="pt-8 text-center">
        <h2 className="text-3xl font-bold text-foreground mb-4">Our Vision</h2>
        <p className="text-lg text-foreground">
          We're building more than just a search tool. We envision a future where you can find anything in your local area with a simple search, get smart recommendations, and feel more connected to the businesses in your neighborhood. Partle is a step towards a more efficient and sustainable local economy.
        </p>
      </div>
    </div>
  );
};

export default About;
