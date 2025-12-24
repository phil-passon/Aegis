# 🛡️ Aegis Discord Bot
Aegis is a professional-grade Discord utility designed to streamline server management, facilitate private support, and enhance community engagement. Built with `discord.py`, it utilizes modern slash commands and a modular cog architecture.

---
##  Key Features
### 🛡️ Professional Moderation
Take full control of your server security with tools designed for efficiency and safety.
* **Permission-Locking:** Commands are restricted to users with the `StaffPerms` role.
* **Standard Actions:** Efficient `/kick`, `/ban`, and `/unban` (via ID) functionality.
* **Channel Management:** Toggle `/lockdown` to silence `@everyone`, or set `/slowmode` for chat pacing.
* **The Nuke Tool:** Instantly clear a channel's history by recreating it with identical settings using `/nuke`.
* **Bulk Clear:** Delete up to 100 messages at once to clean up spam.
### 🎫 Integrated Ticket System
Provide high-quality support with a dedicated ticket environment.
* **Automated Setup:** Automatically creates a "Tickets" category and private channels.
* **Privacy Focused:** Only the user and the staff team can view the created ticket.
* **Anti Spam:** Users can only create one ticket at a time.
* **One-Command Closure:** Use `/close` or press the Close Ticket button to securely delete the ticket channel once the query is resolved.
### 🎨 Advanced Embed Creator
Stop sending plain text. Aegis includes a built-in **Embed Modal** for staff.
* **Interactive Form:** Input titles, descriptions, and image URLs via a native Discord popup.
* **Customization:** Supports Author icons, Thumbnails, and large Main Images for professional announcements.

<p align="center">
  <img height="200" src="https://iili.io/fGoh6iJ.png" width="160" alt="Aegis Embed Modal"/>
  <br>
  <i>The Aegis /embed interactive modal form.</i>
</p>

### 📊 Server & User Insights
Get deep-dive data on your community at a glance.
* **Whois:** View detailed member profiles, including account age, join date, and role hierarchy.
* **Server Info:** Monitor boost levels, member counts (humans vs. bots), and verification settings.
### 🎮 Community Engagement
Keep your members active with interactive "Fun" commands.
* **Dynamic Polls:** Create polls with up to 10 options; the bot automatically adds reaction emojis for voting.
* **Classic Games:** Play Rock-Paper-Scissors, Flip a Coin, or try your luck at Russian Roulette.
* **Magic 8-Ball:** A randomized response engine for community questions.

---
## 🛠️ Technical Specifications
* **Language:** Python 3.10+
* **Library:** [discord.py](https://github.com/Rapptz/discord.py)
* **Architecture:** Cog-based (Moderation, Info, Fun, Support)
* **Features:** Slash Commands, Modals, Persistent Views, and Background Tasks.

---
## ⚙️ Quick Start
**Prerequisites:**
   * Python installed on your system.
   * A Discord Bot Token from the [Developer Portal](https://discord.com/developers/applications).
**Installation:** 
### 1. Clone the repository:
```bash  
    git clone https://github.com/phil-passon/Aegis.git
    cd Aegis
```
### 2. Install dependencies:
```bash
  pip install discord.py python-dotenv
```
### 3. Configure Environment: Create a ``.env`` file in the root directory and add your bot token:
```python
DISCORD_BOT_TOKEN=your_token_here
```
### 4. Run the Bot:
```bash
  python Main.py
```