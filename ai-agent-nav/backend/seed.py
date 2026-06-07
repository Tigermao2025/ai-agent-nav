"""
数据库初始化 + 种子数据
运行: python seed.py
"""
import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'nav.db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("已删除旧数据库")

    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT DEFAULT '📁',
            sort_order INTEGER DEFAULT 0
        );

        CREATE TABLE sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT DEFAULT '',
            badge TEXT DEFAULT '',
            domain TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        );

        CREATE TABLE admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    """)

    cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)",
                   ('admin', hash_password('admin123')))

    # === 分类和站点数据 ===
    data = [
        {
            "name": "大语言模型 / 对话AI",
            "icon": "💬",
            "sort_order": 1,
            "sites": [
                ("DeepSeek", "https://www.deepseek.com", "深度求索 · 开源大模型，推理能力极强，性价比之王", "🔥", "deepseek.com"),
                ("Kimi", "https://kimi.moonshot.cn", "月之暗面 · 超长上下文窗口，擅长文档分析", "", "kimi.moonshot.cn"),
                ("文心一言", "https://yiyan.baidu.com", "百度 · 知识增强大语言模型，多模态能力", "", "yiyan.baidu.com"),
                ("通义千问", "https://tongyi.aliyun.com", "阿里云 · Qwen系列模型，开源生态完善", "", "tongyi.aliyun.com"),
                ("豆包", "https://www.doubao.com", "字节跳动 · 对话AI助手，集成在抖音生态", "", "doubao.com"),
                ("腾讯混元", "https://hunyuan.tencent.com", "腾讯 · 全链路自研大模型，多模态应用", "", "hunyuan.tencent.com"),
                ("智谱清言", "https://chatglm.cn", "智谱AI · GLM系列，学术与商业并重", "🔥", "chatglm.cn"),
                ("讯飞星火", "https://xinghuo.xfyun.cn", "科大讯飞 · 语音交互优势，教育场景深耕", "", "xinghuo.xfyun.cn"),
                ("百川智能", "https://www.baichuan-ai.com", "王小川创立，搜索增强大模型", "", "baichuan-ai.com"),
                ("MiniMax", "https://www.minimaxi.com", "万亿参数MoE，海螺AI/Talkie", "", "minimaxi.com"),
                ("零一万物", "https://www.lingyiwanwu.com", "李开复创立，Yi系列大模型", "", "lingyiwanwu.com"),
                ("阶跃星辰", "https://www.stepfun.com", "Step系列多模态大模型，AI视频生成", "", "stepfun.com"),
                ("360智脑", "https://ai.360.com", "360 · 大语言模型，集成AI搜索与安全能力", "", "ai.360.com"),
                ("书生·浦语 InternLM", "https://internlm.org", "上海AI实验室 · 开源全能大模型，支持超长文本", "", "internlm.org"),
                ("元象 XVERSE", "https://www.xverse.cn", "元象科技 · 开源大模型，支持多语言", "", "xverse.cn"),
            ]
        },
        {
            "name": "AI Agent 平台",
            "icon": "🛠️",
            "sort_order": 2,
            "sites": [
                ("扣子 Coze", "https://www.coze.cn", "字节跳动 · 零代码搭建AI Bot，插件市场丰富", "🔥", "coze.cn"),
                ("Dify", "https://dify.ai", "开源LLM应用开发平台，Agent + RAG + Workflow", "🔥", "dify.ai"),
                ("百度智能体", "https://agents.baidu.com", "百度 · 文心智能体平台，零门槛创建Agent", "", "agents.baidu.com"),
                ("阿里百炼", "https://bailian.aliyun.com", "阿里云 · 大模型服务平台，Agent应用构建", "", "bailian.aliyun.com"),
                ("腾讯元器", "https://yuanqi.tencent.com", "腾讯 · AI智能体创建与分发平台", "", "yuanqi.tencent.com"),
                ("FastGPT", "https://fastgpt.in", "开源知识库问答 + 工作流编排平台", "", "fastgpt.in"),
                ("LangChain 中文", "https://www.langchain.com.cn", "LangChain 中文社区，LLM应用开发框架", "", "langchain.com.cn"),
                ("We0", "https://www.we0.ai", "Wx0 · 数据驱动的AI Agent工作流平台", "", "we0.ai"),
            ]
        },
        {
            "name": "AI 图像 / 视频生成",
            "icon": "🎨",
            "sort_order": 3,
            "sites": [
                ("即梦 AI", "https://jimeng.jianying.com", "字节跳动 · AI图片/视频生成，剪映生态", "🔥", "jimeng.jianying.com"),
                ("可灵 AI", "https://kling.kuaishou.com", "快手 · 领先的AI视频生成，图生视频效果惊艳", "🔥", "kling.kuaishou.com"),
                ("通义万相", "https://tongyi.aliyun.com/wanxiang", "阿里云 · AI图片生成，创意绘画工具", "", "tongyi.aliyun.com/wanxiang"),
                ("文心一格", "https://yige.baidu.com", "百度 · AI艺术与创意图片生成", "", "yige.baidu.com"),
                ("Vidu", "https://www.vidu.studio", "生数科技 · 文本/图片生成视频", "", "vidu.studio"),
                ("DAMO 视频生成", "https://cogvideo.damo.alibaba.com", "阿里达摩院 · 文本生成视频研究", "", "cogvideo.damo.alibaba.com"),
                ("PixVerse", "https://pixverse.ai", "爱诗科技 · AI视频生成工具", "", "pixverse.ai"),
                ("腾讯智影", "https://zenvideo.qq.com", "腾讯 · AI视频创作平台，支持数字人播报", "", "zenvideo.qq.com"),
                ("稿定AI", "https://www.gaoding.com/ai", "稿定设计 · AI图像生成，电商视觉工具", "", "gaoding.com/ai"),
            ]
        },
        {
            "name": "AI 编程助手",
            "icon": "⌨️",
            "sort_order": 4,
            "sites": [
                ("通义灵码", "https://tongyi.aliyun.com/lingma", "阿里云 · AI 编码助手，支持多种IDE", "", "tongyi.aliyun.com/lingma"),
                ("百度 Comate", "https://comate.baidu.com", "百度 · 智能代码助手，支持主流IDE", "", "comate.baidu.com"),
                ("讯飞 iFlyCode", "https://iflycode.xfyun.cn", "科大讯飞 · AI 编程辅助工具", "", "iflycode.xfyun.cn"),
                ("腾讯 Coding", "https://www.tencentcloud.com/zh/products/coding", "腾讯 · DevOps + AI辅助开发平台", "", "tencentcloud.com"),
                ("CodeGeeX", "https://codegeex.cn", "智谱AI · 免费AI编程助手，支持多种IDE", "🔥", "codegeex.cn"),
                ("MarsCode", "https://www.marscode.cn", "字节跳动 · 云端AI编程平台", "", "marscode.cn"),
            ]
        },
        {
            "name": "AI 搜索 & 效率工具",
            "icon": "🔍",
            "sort_order": 5,
            "sites": [
                ("apikey.fun", "https://apikey.fun/dashboard", "AI API密钥管理面板 · 一站式获取各大模型API", "API", "apikey.fun"),
                ("秘塔 AI", "https://metaso.cn", "AI搜索引擎，结构化答案，学术搜索能力强", "🔥", "metaso.cn"),
                ("天工 AI", "https://www.tiangong.cn", "昆仑万维 · AI搜索+对话，多模态融合", "", "tiangang.cn"),
                ("360 AI 搜索", "https://so.360.com", "360 · AI搜索引擎，安全领域深耕", "", "so.360.com"),
                ("纳米搜索", "https://www.nami.so", "360 · 新一代AI搜索产品", "", "nami.so"),
                ("剪映", "https://www.jianying.com", "字节跳动 · AI视频剪辑工具，功能强大", "", "jianying.com"),
                ("夸克AI搜索", "https://www.quark.cn", "夸克浏览器 · AI搜索引擎，支持深度问答", "", "quark.cn"),
                ("知乎直答", "https://www.zhihu.com/ai", "知乎 · AI搜索问答，知识社区驱动", "", "zhihu.com/ai"),
            ]
        },
        {
            "name": "AI 音频 / 语音",
            "icon": "🎵",
            "sort_order": 6,
            "sites": [
                ("讯飞智作", "https://www.iflyrec.com", "科大讯飞 · AI语音合成，配音，虚拟主播", "", "iflyrec.com"),
                ("天工音乐", "https://skymusic.com.cn", "昆仑万维 · AI音乐生成平台", "", "skymusic.com.cn"),
                ("Suno", "https://suno.com", "AI音乐生成，支持中文歌词创作", "", "suno.com"),
                ("海绵音乐", "https://jianying.com", "字节跳动 · AI音乐创作工具", "", "jianying.com"),
                ("网易天音", "https://music.163.com/ai", "网易云音乐 · AI音乐创作平台", "", "music.163.com/ai"),
            ]
        },
        {
            "name": "AI 开源社区 & 模型",
            "icon": "📦",
            "sort_order": 7,
            "sites": [
                ("Hugging Face", "https://huggingface.co", "全球最大AI模型社区，模型/数据集托管", "", "huggingface.co"),
                ("ModelScope", "https://modelscope.cn", "阿里达摩院 · 国内AI模型开源社区", "国内", "modelscope.cn"),
                ("启智社区", "https://openi.pcl.ac.cn", "鹏城实验室 · 开源AI算力与模型平台", "", "openi.pcl.ac.cn"),
                ("GitHub", "https://github.com", "开源代码托管，AI项目汇聚地", "", "github.com"),
                ("Gitee", "https://gitee.com", "码云 · 国内最大代码托管平台，开源AI项目汇聚", "国内", "gitee.com"),
                ("AI Studio", "https://aistudio.baidu.com", "百度 · 深度学习平台，含模型训练与社区", "", "aistudio.baidu.com"),
                ("阿里云天池", "https://tianchi.aliyun.com", "阿里云 · AI竞赛与开源社区", "", "tianchi.aliyun.com"),
            ]
        },
        {
            "name": "AI 资讯 & 社区",
            "icon": "📰",
            "sort_order": 8,
            "sites": [
                ("36氪 AI", "https://www.36kr.com/info/AI", "AI行业资讯，创业公司报道", "", "36kr.com"),
                ("BAAI 智源社区", "https://hub.baai.ac.cn", "北京智源研究院 · AI学术社区", "", "hub.baai.ac.cn"),
                ("量子位", "https://www.qbitai.com", "AI科技媒体，前沿报道", "", "qbitai.com"),
                ("机器之心", "https://www.jiqizhixin.com", "专业AI媒体，技术深度分析", "", "jiqizhixin.com"),
                ("新智元", "https://www.xinzhiyuan.com", "专注AI前沿技术与产业报道", "", "xinzhiyuan.com"),
            ]
        },
        {
            "name": "AI 办公效率",
            "icon": "📄",
            "sort_order": 9,
            "sites": [
                ("WPS AI", "https://www.wps.com/ai", "WPS Office · AI写作、智能表格、PPT生成", "🔥", "wps.com/ai"),
                ("飞书智能伙伴", "https://www.feishu.cn/ai", "飞书 · AI助手，文档生成、会议纪要、对话", "", "feishu.cn/ai"),
                ("钉钉AI", "https://www.dingtalk.com/ai", "钉钉 · AI助手，写文档、会议纪要、审批", "", "dingtalk.com/ai"),
                ("讯飞听见", "https://www.iflyrec.com", "科大讯飞 · AI语音转文字、会议记录", "", "iflyrec.com"),
                ("石墨文档AI", "https://shimo.im/ai", "石墨 · AI辅助写作与文档协作", "", "shimo.im/ai"),
                ("腾讯文档AI", "https://docs.qq.com/ai", "腾讯 · AI写作、智能排版与协作", "", "docs.qq.com/ai"),
            ]
        },
        {
            "name": "AI API 聚合平台",
            "icon": "🔌",
            "sort_order": 10,
            "sites": [
                ("硅基流动", "https://siliconflow.cn", "多种大模型API聚合，支持国内外主流模型", "🔥", "siliconflow.cn"),
                ("百度AI开放平台", "https://ai.baidu.com", "聚合百度多种AI能力API，模型服务", "", "ai.baidu.com"),
                ("阿里云AI", "https://ai.aliyun.com", "阿里云AI平台，通义系列API服务", "", "ai.aliyun.com"),
                ("腾讯云AI", "https://cloud.tencent.com/product/ai", "腾讯云AI服务聚合，大模型API", "", "cloud.tencent.com/product/ai"),
                ("华为云AI", "https://www.huaweicloud.com/ai", "华为云AI能力聚合，盘古大模型API", "", "huaweicloud.com/ai"),
            ]
        },
        {
            "name": "AI 设计工具",
            "icon": "🎯",
            "sort_order": 11,
            "sites": [
                ("稿定设计", "https://www.gaoding.com", "在线AI设计平台，智能抠图、海报生成", "", "gaoding.com"),
                ("创客贴", "https://www.chuangkit.com", "AI辅助平面设计平台，模板丰富", "", "chuangkit.com"),
                ("Canva 可画", "https://www.canva.cn", "国际AI设计工具中文版，海量模板", "", "canva.cn"),
                ("阿里鹿班", "https://luban.aliyun.com", "阿里AI设计平台，自动生成电商海报", "", "luban.aliyun.com"),
            ]
        },
    ]

    for cat in data:
        cursor.execute(
            "INSERT INTO categories (name, icon, sort_order) VALUES (?, ?, ?)",
            (cat["name"], cat["icon"], cat["sort_order"])
        )
        cat_id = cursor.lastrowid
        for i, site in enumerate(cat["sites"]):
            cursor.execute(
                "INSERT INTO sites (category_id, name, url, description, badge, domain, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (cat_id, site[0], site[1], site[2], site[3], site[4], i)
            )

    conn.commit()
    conn.close()

    # 统计
    total_cats = len(data)
    total_sites = sum(len(c["sites"]) for c in data)
    print(f"✅ 数据库初始化完成！")
    print(f"   分类: {total_cats} 个")
    print(f"   站点: {total_sites} 个")
    print(f"   管理员: admin / admin123")

if __name__ == "__main__":
    init_db()
