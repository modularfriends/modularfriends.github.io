# Zero-cost newsletter form (testing only)

This branch prototypes an on-site email capture for Modular Friends through FormSubmit's free AJAX endpoint. The form sends address and consent to the official Modular Friends Gmail. It is NOT a complete opt-in marketing-list manager and does NOT send double-opt-in confirmations. Submissions must not be treated as active subscribers without additional validation and appropriate consent record storage.

**Important**: FormSubmit may keep copies of submissions. The standard Gmail inbox is not equivalent to a secure contact-list provider. Do not publicly activate until:
- The official inbox receives the activation email and is authorized.
- An internal test submission is received, exact fields (email and consent) recorded.
- The list importing process and unsubscribe handling are documented and confirmed to work.
- An actual sender can safely send emails to consented subscribers (Luma newsletter is available free, subject to send cap and unlock).
- Appropriate disclosure is added to the privacy page.
- The live site's Luma fallback remains active until that point.

The smoke-test workflow triggers a SINGLE consented submission using only the community's own official public email address, with no private person data. Once completed, remove the workflow to avoid unintended retries.
