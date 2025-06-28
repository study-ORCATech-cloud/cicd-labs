# Lab Instructions for LAB09: ArgoCD Notifications - Comprehensive Monitoring and Alerting

This document provides detailed step-by-step instructions for setting up comprehensive ArgoCD notifications across multiple channels including email, Slack, webhooks, and Microsoft Teams. You'll learn how to create intelligent alerting that keeps your team informed without causing alert fatigue.

We will start by setting up the notifications controller, then configure email notifications as the primary method, create custom templates, and test various notification scenarios. Additional channels like Slack are covered as optional advanced topics.

---

## 🚀 Lab Steps

### Phase 1: Copy Lab Materials and Install ArgoCD Notifications Controller

**1. Create Directory Structure:**
   ```bash
   mkdir -p notification-controller notification-configs/{notifiers,templates,triggers} secrets test-scenarios scripts
   ```

**2. Copy ArgoCD Notifications Controller Configuration:**
   * Copy the notifications controller deployment:
      ```bash
      cp notification-controller/argocd-notifications-controller.yaml ./
      ```
   
   * Review the controller configuration:
      ```bash
      cat notification-controller/argocd-notifications-controller.yaml
      ```

   * Copy RBAC for notifications controller:
      ```bash
      cp notification-controller/argocd-notifications-rbac.yaml ./
      ```
   
   * Review the RBAC configuration:
      ```bash
      cat notification-controller/argocd-notifications-rbac.yaml
      ```

**3. Deploy Notifications Controller:**
   ```bash
   kubectl apply -f notification-controller/argocd-notifications-rbac.yaml
   kubectl apply -f notification-controller/argocd-notifications-controller.yaml
   ```

**4. Verify Installation:**
   ```bash
   kubectl get pods -n argocd | grep notifications
   kubectl logs -n argocd deployment/argocd-notifications-controller
   ```

### Phase 2: Set Up Email Integration

**5. Copy and Configure Email Credentials:**
   ```bash
   cp secrets/email-credentials-secret.yaml ./
   ```

**6. Configure Your Email Settings:**
   ```bash
   # Edit the email credentials file with your email details
   nano secrets/email-credentials-secret.yaml
   
   # For Gmail users:
   # 1. Use your Gmail address for email-username
   # 2. Create an App Password: Google Account → Security → App passwords
   # 3. Use the App Password (not your regular password) for email-password
   # 4. Enable 2-factor authentication if not already enabled
   ```

**7. Review Email Configuration:**
   ```bash
   cat secrets/email-credentials-secret.yaml
   ```

**8. Apply Email Secret:**
   ```bash
   kubectl apply -f secrets/email-credentials-secret.yaml
   ```

**9. Verify Secret Creation:**
   ```bash
   kubectl get secret argocd-notifications-secret -n argocd
   ```

> **📧 Email Setup Help:**
> - **Gmail**: Use App Passwords (Google Account → Security → App passwords)
> - **Outlook**: Use App Passwords (Microsoft Account → Security → App passwords)  
> - **Yahoo**: Use App Passwords (Yahoo Account → Security → App passwords)
> - **Custom SMTP**: Use your regular email credentials and update SMTP settings in master config

### Phase 3: Copy and Configure Notification Templates

**9. Copy Sync Event Templates:**
   ```bash
   cp notification-configs/templates/app-sync-templates.yaml ./
   ```

**10. Review Sync Templates:**
   ```bash
   cat notification-configs/templates/app-sync-templates.yaml
   ```

**11. Copy Health Event Templates:**
   ```bash
   cp notification-configs/templates/app-health-templates.yaml ./
   ```

**12. Review Health Templates:**
   ```bash
   cat notification-configs/templates/app-health-templates.yaml
   ```

**13. Copy Environment-Specific Templates:**
   ```bash
   cp notification-configs/templates/environment-templates.yaml ./
   ```

**14. Review Environment Templates:**
   ```bash
   cat notification-configs/templates/environment-templates.yaml
   ```

### Phase 4: Configure Notification Triggers

**15. Copy Production Triggers:**
   ```bash
   cp notification-configs/triggers/production-triggers.yaml ./
   ```

**16. Review Production Triggers:**
   ```bash
   cat notification-configs/triggers/production-triggers.yaml
   ```

**17. Copy Staging Triggers:**
   ```bash
   cp notification-configs/triggers/staging-triggers.yaml ./
   ```

**18. Review Staging Triggers:**
   ```bash
   cat notification-configs/triggers/staging-triggers.yaml
   ```

**19. Copy Global Triggers:**
   ```bash
   cp notification-configs/triggers/global-triggers.yaml ./
   ```

**20. Review Global Triggers:**
   ```bash
   cat notification-configs/triggers/global-triggers.yaml
   ```

### Phase 5: Deploy Master Notifications Configuration

**21. Copy Master Configuration:**
   ```bash
   cp notification-configs/master-notifications-config.yaml ./
   ```

**22. Review Master Configuration:**
   ```bash
   cat notification-configs/master-notifications-config.yaml
   ```

**23. Apply Master Configuration:**
   ```bash
   kubectl apply -f notification-configs/master-notifications-config.yaml
   ```

**24. Verify Configuration:**
   ```bash
   kubectl get configmap argocd-notifications-cm -n argocd -o yaml
   ```

### Phase 6: Configure Additional Notifiers (Optional)

**25. Copy Slack Notifier:**
   ```bash
   cp notification-configs/notifiers/slack-notifier.yaml ./
   ```

**26. Copy Email Notifier:**
   ```bash
   cp notification-configs/notifiers/email-notifier.yaml ./
   ```

**27. Copy Webhook Notifier:**
   ```bash
   cp notification-configs/notifiers/webhook-notifier.yaml ./
   ```

**28. Copy Teams Notifier:**
   ```bash
   cp notification-configs/notifiers/teams-notifier.yaml ./
   ```

**29. Review Additional Notifiers:**
   ```bash
   cat notification-configs/notifiers/slack-notifier.yaml
   cat notification-configs/notifiers/email-notifier.yaml
   cat notification-configs/notifiers/webhook-notifier.yaml
   cat notification-configs/notifiers/teams-notifier.yaml
   ```

### Phase 7: Deploy Test Applications

**30. Copy Test Applications:**
   ```bash
   cp test-scenarios/test-app-healthy.yaml ./
   cp test-scenarios/test-app-sync-failed.yaml ./
   cp test-scenarios/test-app-production.yaml ./
   ```

**31. Review Test Applications:**
   ```bash
   cat test-scenarios/test-app-healthy.yaml
   cat test-scenarios/test-app-sync-failed.yaml
   cat test-scenarios/test-app-production.yaml
   ```

**32. Update Email Addresses in Test Applications:**
   ```bash
   # Replace the placeholder email with your actual email address
   YOUR_EMAIL="your-actual-email@gmail.com"
   
   # Update all test application files
   sed -i "s|your-email@gmail.com|$YOUR_EMAIL|g" test-scenarios/test-app-healthy.yaml
   sed -i "s|your-email@gmail.com|$YOUR_EMAIL|g" test-scenarios/test-app-production.yaml
   sed -i "s|your-email@gmail.com|$YOUR_EMAIL|g" test-scenarios/test-app-sync-failed.yaml
   
   # Verify the changes
   grep "notifications.argoproj.io" test-scenarios/test-app-healthy.yaml
   ```

**33. Deploy Test Applications:**
   ```bash
   kubectl apply -f test-scenarios/test-app-healthy.yaml
   kubectl apply -f test-scenarios/test-app-production.yaml
   ```

**34. Verify Test Applications:**
   ```bash
   kubectl get applications -n argocd | grep test-notifications
   ```

### Phase 8: Test Notification Scenarios

**35. Use Setup Script (Optional):**
   ```bash
   cp scripts/setup-notifications.sh ./
   chmod +x scripts/setup-notifications.sh
   ./scripts/setup-notifications.sh
   ```

**36. Use Test Script:**
   ```bash
   cp scripts/test-notifications.sh ./
   chmod +x scripts/test-notifications.sh
   ./scripts/test-notifications.sh
   ```

**37. Monitor Notifications:**
   ```bash
   # Watch controller logs for notification delivery
   kubectl logs -n argocd deployment/argocd-notifications-controller -f
   
   # Check application status
   kubectl get applications -n argocd
   
   # Trigger manual sync for production app (should send email notification)
   kubectl patch app test-notifications-production -n argocd --type merge -p '{"operation":{"sync":{}}}'
   ```

**38. Test Failure Scenarios:**
   ```bash
   # Deploy failing application
   kubectl apply -f test-scenarios/test-app-sync-failed.yaml
   
   # Watch for failure notifications in your email
   kubectl get applications -n argocd test-notifications-sync-fail
   
   # Check your email inbox for sync failure notifications
   ```

### Phase 9: Advanced Testing and Validation

**39. Test Environment-Based Routing:**
   ```bash
   # Check production alerts (should trigger urgent emails)
   kubectl get app test-notifications-production -n argocd -o yaml | grep -A 10 status
   
   # Check staging notifications (should trigger standard emails)
   kubectl get app test-notifications-healthy -n argocd -o yaml | grep -A 10 status
   ```

**40. Validate Notification Delivery:**
   ```bash
   # Check controller metrics
   kubectl port-forward -n argocd svc/argocd-notifications-controller-metrics 9001:9001 &
   curl http://localhost:9001/metrics | grep notification
   
   # Check controller logs for email delivery status
   kubectl logs -n argocd deployment/argocd-notifications-controller | grep -i email
   ```

**41. Test Manual Triggers:**
   ```bash
   # Add manual notification annotation for email
   kubectl annotate app test-notifications-healthy -n argocd \
     notifications.argoproj.io/subscribe.on-sync-succeeded.email="your-actual-email@gmail.com"
   
   # Trigger sync (should send email notification)
   kubectl patch app test-notifications-healthy -n argocd --type merge -p '{"operation":{"sync":{}}}'
   
   # Check your email inbox for the sync success notification
   ```

---

## 🚀 Optional: Advanced Slack Integration

If you have access to a Slack workspace and want to add Slack notifications in addition to email, follow these optional steps:

### **Configure Slack Webhook:**

**A1. Create Slack Webhook (Prerequisites):**
   * Go to your Slack workspace
   * Navigate to Apps → Incoming Webhooks  
   * Click "Add to Slack" and select a channel (e.g., #argocd-alerts)
   * Copy the webhook URL (format: https://hooks.slack.com/services/...)

**A2. Copy and Configure Slack Secret:**
   ```bash
   cp secrets/slack-webhook-secret.yaml ./
   ```

**A3. Update Slack Webhook URL:**
   ```bash
   # Replace with your actual Slack webhook URL  
   SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   sed -i "s|YOUR_SLACK_WEBHOOK_URL_HERE|$SLACK_WEBHOOK|g" secrets/slack-webhook-secret.yaml
   ```

**A4. Apply Slack Secret:**
   ```bash
   kubectl apply -f secrets/slack-webhook-secret.yaml
   ```

### **Add Slack Service to Master Config:**

**A5. Update Master Configuration:**
   ```bash
   # Add Slack service configuration to existing email config
   kubectl patch configmap argocd-notifications-cm -n argocd --patch '
   data:
     service.slack: |
       token: $slack-webhook-url'
   ```

### **Add Slack Templates:**

**A6. Add Slack Templates:**
   ```bash
   # Add Slack templates for key events
   kubectl patch configmap argocd-notifications-cm -n argocd --patch '
   data:
     template.app-sync-succeeded-slack: |
       slack:
         title: "✅ Application Synced Successfully"
         text: |
           Application **{{.app.metadata.name}}** synced to **{{.app.spec.destination.namespace}}**
           Environment: {{.app.metadata.labels.environment | default "unknown"}}
         color: "good"'
   ```

### **Update Application Annotations for Dual Notifications:**

**A7. Add Slack Subscriptions:**
   ```bash
   # Add Slack notifications alongside existing email notifications
   kubectl annotate app test-notifications-healthy -n argocd \
     notifications.argoproj.io/subscribe.on-sync-succeeded.slack=""
   
   kubectl annotate app test-notifications-production -n argocd \
     notifications.argoproj.io/subscribe.on-production-issue.slack=""
   ```

**A8. Test Dual Notifications:**
   ```bash
   # Trigger sync to test both email and Slack notifications
   kubectl patch app test-notifications-healthy -n argocd --type merge -p '{"operation":{"sync":{}}}'
   
   # Check both your email inbox and Slack channel for notifications
   ```

> **💡 Pro Tip:** With dual notifications configured, you can use email for detailed logs and Slack for quick team alerts, providing comprehensive coverage for your notification strategy.

---

## 🧪 Validation Checklist

### ✅ **Controller Installation**
- [ ] Notifications controller pod is running
- [ ] Controller logs show no errors
- [ ] RBAC permissions are correctly applied
- [ ] Metrics endpoint is accessible

### ✅ **Email Integration**
- [ ] Email credentials secret is created with valid app password
- [ ] Email service configuration is applied
- [ ] SMTP connection can be established
- [ ] Email templates render correctly

### ✅ **Template Configuration**
- [ ] Sync success templates work
- [ ] Sync failure templates work
- [ ] Health degradation templates work
- [ ] Environment-specific templates work
- [ ] Rich formatting (attachments, colors) displays correctly

### ✅ **Trigger Configuration**
- [ ] Production triggers fire for production apps
- [ ] Staging triggers fire for staging apps
- [ ] Global triggers work across environments
- [ ] Label-based filtering works correctly

### ✅ **Test Application Deployment**
- [ ] Healthy test app deploys successfully
- [ ] Production test app triggers appropriate notifications
- [ ] Failing test app triggers failure notifications
- [ ] Application annotations are correctly configured

### ✅ **Notification Delivery**
- [ ] Sync success notifications arrive in email inbox
- [ ] Sync failure notifications arrive in email inbox  
- [ ] Health status notifications arrive in email inbox
- [ ] Production alerts have urgent subject lines
- [ ] Environment-specific routing works (staging vs production emails)

### ✅ **Advanced Scenarios**
- [ ] Label-based notification routing
- [ ] Manual trigger annotations work
- [ ] Multiple notification channels (if configured)
- [ ] Notification escalation for production
- [ ] Template customization works

---

## 🧹 Cleanup

**42. Use Cleanup Script:**
   ```bash
   cp scripts/cleanup-notifications.sh ./
   chmod +x scripts/cleanup-notifications.sh
   ./scripts/cleanup-notifications.sh
   ```

**43. Manual Cleanup (Alternative):**
   ```bash
   # Remove test applications
   kubectl delete -f test-scenarios/ --ignore-not-found=true
   
   # Remove notifications configuration
   kubectl delete -f notification-configs/master-notifications-config.yaml --ignore-not-found=true
   
   # Remove email secrets
   kubectl delete -f secrets/email-credentials-secret.yaml --ignore-not-found=true
   
   # Remove controller
   kubectl delete -f notification-controller/ --ignore-not-found=true
   
   # Clean up test namespaces
   kubectl delete namespace test-notifications test-notifications-fail test-notifications-prod --ignore-not-found=true
   ```

**44. Verify Cleanup:**
   ```bash
   kubectl get pods -n argocd | grep notifications
   kubectl get applications -n argocd | grep test-notifications
   kubectl get configmap argocd-notifications-cm -n argocd
   ```

---

## 🎯 Key Learning Outcomes

By completing this lab, you have learned:

1. **ArgoCD Notifications Architecture**: Understanding the notifications controller, templates, triggers, and services
2. **Multi-Channel Integration**: Configuring email, Slack, webhooks, and Teams notifications
3. **Template Customization**: Creating rich, contextual notification templates with dynamic content
4. **Intelligent Triggering**: Implementing environment-based and label-based notification routing
5. **Production Readiness**: Setting up escalation, alert fatigue prevention, and monitoring
6. **Testing Strategies**: Validating notification delivery and troubleshooting issues
7. **Operational Excellence**: Implementing notifications that enhance rather than overwhelm team productivity

This comprehensive notifications system ensures your team stays informed about critical GitOps events while maintaining focus on development and operations tasks.

---

## 📚 Additional Resources

- [ArgoCD Notifications Documentation](https://argocd-notifications.readthedocs.io/)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [ArgoCD Templating Guide](https://argocd-notifications.readthedocs.io/en/stable/templates/)
- [Notification Triggers Reference](https://argocd-notifications.readthedocs.io/en/stable/triggers/)
- [Production Notification Best Practices](https://argocd-notifications.readthedocs.io/en/stable/services/overview/) 