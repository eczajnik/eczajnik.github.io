"use strict";

const copyrightYear = document.getElementById("copyright-year");

if (copyrightYear) {
  copyrightYear.textContent = new Date().getFullYear();
}

const emailContact = document.getElementById("email-contact");

if (emailContact) {
  // Obfuscation only deters simple harvesters. This is not encryption.
  const address = ["ZWN6YWpuaWs=", "Z21haWwuY29t"].map(atob).join("@");
  const link = document.createElement("a");
  const arrow = document.createElement("span");
  link.href = "mailto:" + address;
  arrow.textContent = "↗";
  arrow.setAttribute("aria-hidden", "true");
  link.append(address + " ", arrow);
  emailContact.replaceChildren(link);
}
