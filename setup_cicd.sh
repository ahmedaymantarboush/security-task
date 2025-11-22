#!/bin/bash

# Quick Setup Script for GitHub Actions + Vercel CI/CD
# This script helps you set up the automatic deployment pipeline

echo "======================================"
echo "  GitHub Actions + Vercel CI/CD Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get Vercel credentials from local .vercel folder
if [ -f ".vercel/project.json" ]; then
    echo -e "${GREEN}✓ Found Vercel project configuration${NC}"
    PROJECT_ID=$(cat .vercel/project.json | grep -o '"projectId":"[^"]*"' | cut -d'"' -f4)
    ORG_ID=$(cat .vercel/project.json | grep -o '"orgId":"[^"]*"' | cut -d'"' -f4)
    
    echo ""
    echo -e "${BLUE}Your Vercel IDs:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "VERCEL_PROJECT_ID: ${YELLOW}$PROJECT_ID${NC}"
    echo -e "VERCEL_ORG_ID:     ${YELLOW}$ORG_ID${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo -e "${RED}✗ Vercel project not linked. Run 'vercel link' first.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Get your VERCEL_TOKEN:"
echo "   → Visit: https://vercel.com/account/tokens"
echo "   → Click 'Create Token'"
echo "   → Copy the token"
echo ""
echo "2. Add the following secrets to GitHub:"
echo "   → Go to: https://github.com/ahmedaymantarboush/security-task/settings/secrets/actions"
echo "   → Click 'New repository secret'"
echo "   → Add these three secrets:"
echo ""
echo -e "   ${GREEN}Secret 1:${NC}"
echo "   Name:  VERCEL_TOKEN"
echo "   Value: [Your token from step 1]"
echo ""
echo -e "   ${GREEN}Secret 2:${NC}"
echo "   Name:  VERCEL_PROJECT_ID"
echo "   Value: $PROJECT_ID"
echo ""
echo -e "   ${GREEN}Secret 3:${NC}"
echo "   Name:  VERCEL_ORG_ID"
echo "   Value: $ORG_ID"
echo ""
echo "3. Push the workflow to GitHub:"
echo "   git add .github/workflows/deploy.yml CICD_SETUP.md"
echo "   git commit -m \"Add CI/CD pipeline for Vercel deployment\""
echo "   git push origin main"
echo ""
echo "4. Check the deployment:"
echo "   → GitHub Actions: https://github.com/ahmedaymantarboush/security-task/actions"
echo "   → Vercel Dashboard: https://vercel.com/dashboard"
echo ""
echo -e "${GREEN}That's it! Your pipeline will be ready.${NC}"
echo ""
