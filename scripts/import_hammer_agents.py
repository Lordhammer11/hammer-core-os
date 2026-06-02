#!/usr/bin/env python3
"""
Import HaMm3r OS custom agents into Open WebUI.
Run from anywhere — prompts for password, handles token safely via file.
Usage: python3 import_hammer_agents.py
"""

import urllib.request
import urllib.error
import json
import getpass
import os

WEBUI_URL = "http://localhost:3000"
EMAIL = "ronald.majewski@agattackllc.com"
TOKEN_FILE = "/tmp/hammer_token.txt"

AGENTS = [
    {
        "id": "investment-manager",
        "name": "💰 Investment Manager",
        "base_model_id": "llama3.2:latest",
        "system": (
            "You are an expert financial advisor focused on helping Ronald build, manage, and protect his wealth. "
            "You are a business tax strategist who knows loopholes for personal and business taxes. "
            "Specialties: Stock Market Investments, Real Estate (multi-family/commercial), "
            "Wealth Management and Irrevocable Trusts, Tax strategy for SSDI and Veterans. "
            "Provide concise, data-driven, actionable guidance."
        ),
        "desc": "Expert financial advisor — stocks, real estate, wealth & tax strategy",
    },
    {
        "id": "vehicle-tech",
        "name": "🚗 Vehicle Tech",
        "base_model_id": "llama3.2:latest",
        "system": (
            "You are an AI Assistant specialized in vehicle performance, maintenance, and technical research. "
            "Primary vehicle: 2018 Chevrolet Silverado 1500 5.3L. "
            "You provide diagnostics, troubleshooting, maintenance schedules, technical education on "
            "powertrains/suspension/electronics, and step-by-step repair and upgrade guidance."
        ),
        "desc": "Vehicle specialist — 2018 Silverado 5.3L diagnostics & upgrades",
    },
    {
        "id": "va-disability-specialist",
        "name": "🎖️ VA Disability Specialist",
        "base_model_id": "llama3.2:latest",
        "system": (
            "You are an AI Veterans Service Officer (VSO) and Veterans Readiness Counselor (VRC) for Ronald. "
            "Assist with: 1) Disability Claims - Intent to File, Fully Developed Claims, evidence gathering, "
            "VA Ratings/VASRD, Appeals. 2) Chapter 31 VR&E Self-Employment - eligibility, business plan "
            "drafting, Real Estate feasibility, Category I/II. Based on 38 CFR and M28C VR&E Manual. "
            "Always provide actionable chronological checklists."
        ),
        "desc": "VA claims, VR&E Chapter 31, 38 CFR & M28C manual",
    },
    {
        "id": "the-hawk",
        "name": "🦅 The Hawk — Business Coach",
        "base_model_id": "llama3.2:latest",
        "system": (
            "You are a specialized AI Assistant supporting Ronald as a veteran entrepreneur. "
            "Assist with: 1) VR&E interview coaching and communicating VA disability ratings professionally, "
            "2) Self-Employment Plans for Transport/Industrial/Federal Contracts Hauling — business structure, "
            "underwriting, bidding and closing contracts, 3) Professional Grant Writing for SBA, VSBA, FSA, "
            "USDA, 4) Strategic guidance from planning to execution of business goals."
        ),
        "desc": "Veteran entrepreneur — transport, federal contracts, grant writing",
    },
    # HaMm3r's Utility Tool is merged into the OS as a native feature — no agent import needed.
    #     "id": "hammers-utility-tool",
    #     "name": "🔧 HaMm3r's Utility Tool",
    #     "base_model_id": "llama3.2:latest",
    #     "system": "<PASTE SYSTEM PROMPT HERE>",
    #     "desc": "Multi-purpose utility agent",
    # },
]


def get_token(password: str) -> str:
    """Authenticate and return Bearer token, saving to file."""
    data = json.dumps({"email": EMAIL, "password": password}).encode()
    req = urllib.request.Request(
        f"{WEBUI_URL}/api/v1/auths/signin",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        token = json.loads(r.read())["token"]
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token


def verify_auth(token: str) -> bool:
    """Verify token works by hitting /api/v1/users/."""
    req = urllib.request.Request(
        f"{WEBUI_URL}/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            return isinstance(data, (list, dict)) and "detail" not in str(data)[:50]
    except Exception:
        return False


def create_agent(token: str, agent: dict) -> tuple[bool, str]:
    """Create one agent. Returns (success, message)."""
    payload = {
        "id": agent["id"],
        "name": agent["name"],
        "base_model_id": agent["base_model_id"],
        "params": {"system": agent["system"]},
        "meta": {
            "description": agent["desc"],
            "profile_image_url": "/static/claude-bot.svg",
            "capabilities": {"vision": False, "citations": True},
        },
        "is_active": True,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{WEBUI_URL}/api/v1/models/create",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            return True, resp.get("id", str(resp))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        # "already registered" means it was previously imported — not a real error
        if "already registered" in body:
            return True, f"already exists (previously imported)"
        return False, f"HTTP {e.code}: {body[:200]}"


def main():
    print("🔨 HaMm3r OS — Agent Import Script")
    print(f"   Target: {WEBUI_URL}")
    print(f"   User:   {EMAIL}\n")

    # Use existing token if available and valid
    token = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            candidate = f.read().strip()
        if len(candidate) > 100 and verify_auth(candidate):
            token = candidate
            print("✓ Using cached token from /tmp/hammer_token.txt\n")

    if not token:
        password = getpass.getpass("Password: ")
        try:
            token = get_token(password)
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            return

        if not verify_auth(token):
            print("✗ Token verification failed — wrong password?")
            return
        print("✓ Authenticated successfully\n")

    success_count = 0
    for agent in AGENTS:
        ok, msg = create_agent(token, agent)
        icon = "✅" if ok else "❌"
        print(f"{icon} {agent['name']}: {msg}")
        if ok:
            success_count += 1

    print(f"\n{'─'*50}")
    print(f"Done: {success_count}/{len(AGENTS)} agents imported successfully")
    print(f"View at: {WEBUI_URL}/workspace/models")


if __name__ == "__main__":
    main()
