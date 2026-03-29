# 新建文件模板

> 创建新文件时的标准结构，让 AI 生成的代码风格一致。
> **加载时机**：创建新文件时加载。日常修改代码不需要加载。

## Service 模板

```
[填写标准模板代码，如:]

// src/services/[name].service.ts
import { Injectable } from '...'

@Injectable()
export class [Name]Service {
  constructor(private readonly repo: [Name]Repository) {}

  async findById(id: string): Promise<[Name]> { ... }
}
```

## 测试模板

```
[填写标准模板代码，如:]

// tests/[name].test.ts
describe('[Name]Service', () => {
  let service: [Name]Service
  
  beforeEach(() => { ... })
  
  it('should ...', async () => { ... })
})  
```

## [其他类型模板，如: Controller / Middleware / Migration]

```
[填写]
```
