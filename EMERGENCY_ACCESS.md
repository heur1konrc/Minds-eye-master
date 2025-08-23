# 🚨 EMERGENCY ACCESS - Mind's Eye Photography

## CRITICAL: Save this file offline for disaster recovery!

### Emergency URLs (work without admin login):

- **Emergency Backup Portal:** `https://your-site.railway.app/emergency-backup`
- **Emergency Download:** `https://your-site.railway.app/emergency-backup/download`
- **Emergency Restore Guide:** `https://your-site.railway.app/emergency-restore-guide`
- **Force Migration:** `https://your-site.railway.app/debug/force-migration`
- **Volume Info:** `https://your-site.railway.app/debug/volume-info`
- **Database Info:** `https://your-site.railway.app/debug/database-info`

### When to Use Emergency Access:

1. **Admin system is broken** - Can't login to admin dashboard
2. **Site is partially down** - Some features not working
3. **Database corruption** - Images not displaying correctly
4. **Complete disaster** - Need to restore everything

### Emergency Backup Process:

1. Go to `/emergency-backup` (no login required)
2. Click "Download Emergency Backup"
3. Save the ZIP file to multiple locations
4. Follow instructions in EMERGENCY_RESTORE.txt

### Railway Volume Access:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link project
railway login
railway link [your-project-id]

# Mount volume to access files
railway volume mount
```

### Emergency Contacts:

- **Railway Support:** help@railway.app
- **GitHub Support:** support@github.com
- **Project Repository:** https://github.com/heur1konrc/Minds-eye-master

### Backup Schedule Recommendation:

- **Daily:** Use admin backup system
- **Weekly:** Download emergency backup
- **Monthly:** Test restore procedures
- **Quarterly:** Full disaster recovery test

### File Locations in Railway Volume:

- **Database:** `/data/mindseye.db`
- **Images:** `/data/*.jpg`, `/data/*.png`
- **Logs:** Check Railway dashboard

Remember: These emergency routes work even if the main site is completely broken!

