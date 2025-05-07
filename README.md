# Project Requirements

## **Ghor Khoje**

---

### Purpose

To create a platform that simplifies apartment hunting for bachelors in Bangladesh by offering verified listings, connecting them with supportive landlords, and fostering a community for shared living.

---

## Core Requirements

1.  User Roles:

    - Bachelors: Can create profiles, browse listings, and contact landlords.
    - Landlords: Can list properties with details and preferences (e.g., male/female bachelors).

2.  Features for Bachelors:

    - Search and filter listings by location, price, amenities, and gender preference.
    - Option to find shared accommodations or roommates.
    - Bookmark favorite listings.

3.  Features for Landlords:

    - Create property listings with details (photos, rent, location, rules).
    - View inquiries and connect with potential tenants.

4.  Verification System:

    - Verify users (both bachelors and landlords) via NID, phone, or email to build trust.

5.  Chat System:

    - Integrated messaging for secure communication between bachelors and landlords.

6.  Ratings and Reviews:

    - Allow bachelors to review landlords/properties and vice versa.

7.  Community Forum: (Optional)

    - A discussion space for tips, roommate searches, and housing advice.

8.  Admin Panel:

    - Manage users, listings, and disputes.
    - Monitor fraudulent activities and ensure a safe platform.

9.  Localization:

    - Support for Bengali and English languages.
    - Map integration for precise location of listings (Google Maps or OpenStreetMap).

10. Monetization Options:

    - Paid featured listings for landlords.
    - Premium user subscriptions for bachelors to access exclusive listings

---

## Tech Stacke Requirements

- **Frontend**: React.js or Next.js for fast, SEO-friendly interfaces.
- **Backend**: Django/Node.js for a scalable and secure server.
- **Database**: PostgreSQL/MySQL for structured data.
- **APIs**: Google Maps API for location integration, Firebase for notifications.

---

## More Details

## User Roles and Verification System

### 1. User Roles

#### A. **Bachelors**

- **Features:**
  - Create a profile with details like:
    - Name, gender, age, and occupation.
    - Contact information (email, phone number).
    - Preferred location, budget, and type of accommodation.
  - Search and filter listings by:
    - Location, rent range, gender preference, and amenities.
  - Save favorite listings for later.
  - Contact landlords securely through an in-app chat system.
  - Post roommate requirements or shared accommodation requests.
  - Provide reviews/ratings for properties and landlords.

#### B. **Landlords**

- **Features:**
  - Create property listings with details such as:
    - Address, rent, amenities (WiFi, parking, etc.), rules, and photos.
    - Gender preference (male/female bachelors).
  - View and respond to inquiries from bachelors.
  - See tenant ratings and reviews.
  - Option to promote listings for better visibility (paid feature).

#### C. **Admin**

- **Features:**
  - Approve or reject user accounts and property listings.
  - Manage reports on users, landlords, or listings.
  - Monitor the platform for fraud or rule violations.
  - Resolve disputes between users.
  - Oversee the verification process to ensure accuracy and security.

---

### 2. Verification System

#### **Purpose:**

To ensure trust and authenticity, preventing fake accounts or fraudulent listings.

#### **Verification Steps:**

##### A. For Bachelors

1. **Phone Verification:**
   - OTP (One-Time Password) sent to the provided phone number.
2. **Email Verification:**
   - A verification link sent to the registered email.
3. **Identity Verification (Optional):**
   - Upload a scanned copy or photo of the National ID (NID) or passport.
   - Admin manually reviews and approves the document.

##### B. For Landlords

1. **Phone Verification:**
   - OTP (One-Time Password) sent to the provided phone number.
2. **Email Verification:**
   - A verification link sent to the registered email.
3. **Property Ownership Verification (Optional):**
   - Upload documents proving ownership (utility bill, deed, etc.).
   - Admin manually reviews and approves the document.

##### C. Automated Checks

- Ensure submitted phone numbers and emails are not duplicates.
- Flag users with frequent disputes or poor reviews.

---

### 3. User Dashboard Features

#### A. For Bachelors:

- Profile Completion Status (showing pending verifications).
- List of saved properties.
- History of viewed properties.
- Notifications for new listings matching preferences.

#### B. For Landlords:

- Dashboard to manage listed properties.
- Track verification progress of listings.
- Receive tenant inquiries in real-time.
- Analytics on views and inquiries per listing.

#### C. Admin Panel:

- User verification approval/rejection interface.
- Notifications for pending verifications or reports.
- Dashboard with overall platform statistics (users, listings, verifications).

---

### Verification Flow Chart

1. **User Registers** → Profile Completion (Basic Info).
2. **User Submits Phone/Email** → Automated OTP or Link Sent.
3. **Optional Document Submission** → Admin Review.
4. **Final Status:** Verified or Rejected (with reasons).

---

## Amenities

1. Natural Gas
2. Water supply
3. Generator
4. Wifi
5. Dish TV
6. Air conditioning (AC)
7. Water heater
8. Closets
9. Kitchen cabinets
10. Refrigerator
11. Microwave
12. Oven
13. Water filter
14. Rice cooker
15. Washing machine
16. Meal service
17. Private balcony
18. Garage
19. Parking space
20. 24/7 security guard
21. CCTV cameras
22. Intercom
23. Fire extinguisher
24. Smoke detector
25. Elevator / lift
26. Rooftop access
27. Gym
28. Lawn / garden
29. Playground
30. Gas Cylinder

## Place Categories

1. Shared Room
2. Private Room
3. Sublet
4. Flat / Apartment
5. Studio Apartment
6. Duplex (Two-level unit)
7. Full House
8. Penthouse
9. Hostel
10. Bachelor (Male)
11. Bachelor (Female)
12. Family
13. Couple-friendly
14. Girl's Hostel
15. Boy's Hostel
16. Office Space
17. Tin-shed
18. Semi-pucca
19. All Categories
