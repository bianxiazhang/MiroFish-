from app import create_app

app = create_app()

print("Flask 应用的所有路由:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.methods} {rule.rule}")
