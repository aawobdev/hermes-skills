---
name: authjs-v5-nextjs-prisma-setup
title: Auth.js v5 Setup for Next.js 16 + Prisma
version: 1.0.0
description: Implementation steps for Auth.js v5 authentication in Next.js 16 with Prisma and PostgreSQL
---

# Auth.js v5 Setup for Next.js 16 + Prisma

This skill describes the process for implementing Auth.js v5 authentication in a Next.js 16 project with Prisma and PostgreSQL.

## Implementation Steps

1. **Update Prisma Schema**
   - Add Account, Session, User, VerificationToken models
   - Define Role enum (ADMIN, COUNSELLOR, CUSTOMER) 
   - Ensure all required fields are included per Auth.js docs

2. **Create Authentication Configuration**
   - Configure Prisma adapter 
   - Set up Resend provider for magic links
   - Use database session strategy (not JWT)
   - Define pages: signIn -> /login
   - Implement redirect callback to /dashboard

3. **API Route Handler**
   - Create route at src/app/api/auth/[...nextauth]/route.ts
   - Export handler as both GET and POST for Next.js compatibility

4. **API Middleware** 
   - withAuth(handler, options?) - requires authentication, enforces role
   - withOptionalAuth(handler) - attaches user if logged in, continues if not
   - Both return proper 401/403 responses

5. **Login Page**
   - Create src/app/_auth/login/page.tsx
   - Simple centered card with email input and "Send magic link" button
   - Client action form handling

6. **Login Actions**
   - Create src/app/_auth/login/actions.ts
   - Server action for sending magic links (currently logs to console)

## Prisma Models Required

### User Model
```
model User {
  id           String    @id      @default(cuid())
  name         String?
  email        String    @unique
  emailVerified DateTime?
  image        String?
  role         Role
  customerId   String?
  accounts     Account[]
  sessions     Session[]

  @@enum(Role, [
    ADMIN
    COUNSELLOR
    CUSTOMER
  ])
}
```

### Other Required Models:
- Account (with proper relationships)
- Session (with proper relationships)
- VerificationToken 

## Package Requirements
- next-auth@beta
- @next-auth/prisma-adapter  
- resend

## Validation Steps
1. Run `npx prisma validate` - should return success
2. Run `npx prisma migrate dev --name add-auth`
3. Run `npx prisma generate`