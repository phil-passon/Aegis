# 🛡️ Aegis Discord Bot
Aegis is a professional-grade Discord utility designed to streamline server management, facilitate private support, and enhance community engagement. Built with `discord.py`, it utilizes modern slash commands and a modular cog architecture.

---
## Key Features
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
* **One-Command Closure:** Use `/close` or press the Close Ticket button to securely delete the ticket channel.
* **Intern:** Ask Intern Button for some fun answers while waiting to support.
### 🎨 Advanced Embed Creator
Stop sending plain text. Aegis includes a built-in **Embed Modal** for staff.
* **Interactive Form:** Input titles, descriptions, and image URLs via a native Discord popup.
* **Customization:** Supports Author icons, Thumbnails, and large Main Images.
<p align="center">
<img height="200" src="https://iili.io/fGoh6iJ.png" width="160" alt="Aegis Embed Modal"/>
<br>
<i>The Aegis /embed interactive modal form.</i>
</p>

### 📊 Server & User Insights
Get deep-dive data on your community at a glance.
* **Whois:** View detailed member profiles, including account age, join date, and role hierarchy.
* **Server Info:** Monitor boost levels, member counts, and verification settings.
### 🎮 Community Engagement
Keep your members active with interactive "Fun" commands.
* **Dynamic Polls:** Create polls with up to 10 options; the bot automatically adds reaction emojis.
* **Classic Games:** Play Rock-Paper-Scissors, Flip a Coin, or try your luck at Russian Roulette.
* **Magic 8-Ball:** A randomized response engine for community questions.
* **Haunted Channels:** A ghost message will appear sometimes and users have the ability to unlock a rare role.

---
## 📸 Usage Examples
### Moderation in Action
> **Command:** `/kick member:@User reason:Breaking rules`\
> **Outcome:** Aegis verifies the moderator has the `StaffPerms` role and that their hierarchy is higher than the target's before removing the user and logging the reason in a stylized embed.
### Ticket Workflow
Aegis uses a persistent component-based system to handle user queries efficiently:
1. **Initialization:** A user triggers the `/ticket` command.
2. **Creation:** The bot creates a private text channel named `#ticket-[username]` inside a "Tickets" category.
3. **Permissions:** View access is restricted to the **Ticket Owner**, **StaffPerms holders**, and the **Bot**.
4. **Interaction:** The channel is initialized with an embed containing two buttons:
    * **🔒 Close Ticket:** Initiates a 5-second countdown before deleting the channel.
    * **☕ Ask the Intern:** Provides randomized, "unpaid intern" humor to keep users entertained while waiting for staff.
5. **Resolution:** Once the issue is resolved, staff can use `/close` or press the Button to finalize the process.
### Fun & Social
* **`/slap member:@User`** -> 👋 *[Moderator] slapped [User] with **a stale baguette**!*
* **`/poll question:Best Pizza? options_list:Pepperoni, Cheese, Pineapple`** -> Generates a formatted embed with reaction buttons 1️⃣, 2️⃣, and 3️⃣.
* **`/vibecheck`** -> *Current Status: **Main Character Energy 👑***

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
**Installation:** ### 1. Clone the repository:
```bash
    git clone https://github.com/phil-passon/Aegis.git
    cd Aegis
```
### 2. Install dependencies:
```bash
  pip install discord.py python-dotenv
```
### 3. Configure Environment: Create a `.env` file in the root directory:
```env
DISCORD_BOT_TOKEN=your_token_here
```
### 4. Run the Bot:
```bash
  python Main.py
```