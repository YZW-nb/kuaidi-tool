from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

# 快递公司映射表（中文名 -> 快递100编码）
COURIER_MAP = {
    "顺丰": "shunfeng",
    "中通": "zhongtong",
    "圆通": "yuantong",
    "申通": "shentong",
    "韵达": "yunda",
    "京东": "jd",
    "邮政": "youzheng",
    "极兔": "jitu",
    "德邦": "debangwuliu",
    "菜鸟": "cainiao"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    number = request.form['number'].strip()
    company_name = request.form['company']
    company_code = COURIER_MAP.get(company_name)

    if not company_code:
        return "不支持的快递公司", 400

    try:
        # 使用 kuaidi-api.com 的免费接口
        url = "https://www.kuaidi-api.com/api"
        params = {
            "type": company_code,
            "number": number
        }
        res = requests.get(url, params=params, timeout=10).json()
        
        # 如果查询失败，提供友好的错误信息
        if res.get('status') != 'success':
            return render_template('result.html', 
                                   error="查询失败，请确认单号是否正确",
                                   number=number,
                                   company=company_name)
            
        return render_template('result.html', 
                               data=res.get('data', []),
                               number=number, 
                               company=company_name)
    except Exception as e:
        return render_template('result.html', 
                               error=f"查询异常：{str(e)}",
                               number=number,
                               company=company_name)

# 健康检查端点
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))