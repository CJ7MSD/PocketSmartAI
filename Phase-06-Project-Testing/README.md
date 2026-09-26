# Phase 06 – Project Testing

Project: **PocketSmart AI – Your Smart Budget & Recommendation Assistant**

## 1. Test Strategy

Test functional behavior, API integration, authentication, budget handling, UI/UX and error handling.

## 2. Test Cases

1. Authentication | Input: Register with valid data | Expected: Account created; login page shown; email is not auto-pasted | Status: Pass/Retest
2. Authentication | Input: Login with valid credentials | Expected: User enters main Home page; session remains active | Status: Pass/Retest
3. Authentication | Input: Logout | Expected: Session ends and Login becomes available | Status: Pass/Retest
4. Home Planner | Input: Select multiple item types and quantities | Expected: Separate requested item types are searched/recommended | Status: Pass/Retest
5. Home Planner | Input: Budget input | Expected: Recommendation stays budget-aware and reports budget issues clearly | Status: Pass/Retest
6. Party Planner | Input: Guest count + budget | Expected: Party recommendations generated | Status: Pass/Retest
7. Jewelry Planner | Input: Text inputs | Expected: Jewelry recommendations generated | Status: Pass/Retest
8. Jewelry Planner | Input: Optional image input | Expected: Image-aware recommendation flow works when configured | Status: Pass/Retest
9. Live API | Input: SerpApi valid key | Expected: Usable shopping results returned | Status: Pass/Retest
10. AI API | Input: Gemini valid model/key | Expected: Structured AI response returned | Status: Pass/Retest
11. Dashboard | Input: Open while logged in | Expected: No login flicker; stable navigation | Status: Pass/Retest
12. UI/UX | Input: Login/Register pages | Expected: Main navbar hidden; centered PocketSmart branding visible | Status: Pass/Retest

## 3. API Error Tests

Verify invalid Gemini credentials, invalid SerpApi credentials, empty provider results, unsupported/missing product fields, and AI schema/model errors. The application should show a useful diagnostic or fallback behavior rather than exposing secrets.

## 4. Browser Tests

Test registration, login, navigation, planner forms, dashboard, logout, hard refresh, and responsive behavior in the target browser.

## 5. Evidence

For the final submission, add screenshots or short recordings for successful test cases and place them under this phase folder.

