from asyncio.windows_events import NULL
import random
import os

class Field:
    def __init__(self,name,type,remark,cannull=True,default_val=''):
        self.name=name
        self.type=type
        self.remark=remark
        self.cannull=cannull
        self.default_val=default_val
        self.DataType='String'
        self.CsharpType='string'
        if 'date' in type.lower():
            self.DataType='DateTime'
            self.CsharpType='DateTime'
        elif 'int' in type.lower():
            self.DataType='Number'
            self.CsharpType='int'
        elif 'decimal' in type.lower():
            self.DataType='Number'
            self.CsharpType='decimal'
        elif 'float' in type.lower():
            self.DataType='Number'
            self.CsharpType='float'
        else:
            for t in ['nvarchar','text']:
                if t in type.lower():
                    self.DataType='String'
                    self.CsharpType='string'
                    break
                
    @classmethod
    def decimalField(cls, name, remark,  precision:tuple=(18,7),cannull=False, default_val=''):
        return cls(name, f'decimal({precision[0]},{precision[1]})', remark, cannull, default_val)
    
    @classmethod
    def intField(cls, name, remark, cannull=False, default_val=''):
        return cls(name, 'int', remark, cannull, default_val)
    
    @classmethod
    def nvarcharField(cls, name, remark, len=50, cannull=False, default_val=''):
        return cls(name, f'nvarchar({len})', remark, cannull, default_val)
    
    @classmethod
    def datetimeField(cls, name, remark, cannull=False, default_val=''):
        return cls(name, 'datetime', remark, cannull, default_val)
    
    @classmethod
    def dateField(cls, name, remark, cannull=False, default_val=''):
        return cls(name, 'date', remark, cannull, default_val)    
            
class SqlTable:
    def __init__(self,name,key,fields,db):
        self.db = db
        self.name=name
        self.key=key
        self.fields=fields
    
    def getInsertSql(self, row):
        sql_str = None
        try:
            fields_str = ','.join([field.name for field in self.fields])
            values_str = ""
            for field in self.fields:
                value = row[field.remark]
                if 'int' in field.type:
                    values_str = values_str + f" {int(value)},"
                elif 'decimal' in field.type:
                    values_str = values_str + f" {value},"
                else:
                    values_str = values_str + f" '{value}',"
            values_str = values_str[:-1]   
            
            sql_str = f"INSERT INTO dbo.{self.name} ({fields_str}) values ({values_str})"
        except Exception as e:
            print(e)
        finally:
            return sql_str
        
    def getQuerySql(self, conditions:dict=None):
        '''
        获取查询语句
        conditions：查询条件的字典，key:字段， value:具体条件，
        如：{"TimePoint": "> '2023-01-01'}等价于 "and TimePoint>'2023-01-01'“ 
        '''
        fields_str = ','.join([field.name for field in self.fields])
        fields_str = self.key + ',' + fields_str
        sql_str = f"select {fields_str} from {self.db}.dbo.{self.name} where 1=1 "
        if conditions and len(conditions)>0:
            for key,cond in conditions.items():
                # 检查是否有这个字段
                for field in self.fields:
                    if field.name==key:
                        sql_str = sql_str + f" and {key} {cond}"
                        break
                        
        return sql_str
    
    # 生成随机的数据
    def getRandomData(self,nums,isall):
        result=[]
        for i in range(nums):
            unitfields=''
            unitvalues=''
            for field in self.fields:
                if not isall and field.cannull:
                    continue
                unitfields=unitfields+','+field.name
                # 有默认值时用默认值
                if not field.default_val=='':
                    str=",'{0}'".format(field.default_val)
                    if field.DataType=='Number':
                        str=",{0}".format(field.default_val)
                    unitvalues+=str
                # 日期类型 
                elif field.DataType=='DateTime':
                    test_date=",'{0}-{1}-{2} 00:00:00'".format(random.randint(1949,2022),random.randint(1,12),random.randint(1,28))
                    unitvalues+=test_date
                # 字符串类型
                elif field.DataType=='String':
                    test_str=",'测试数据_{0}_{1}-{2}'".format(i,field.name,random.randint(0,10000))
                    unitvalues+=test_str
                # 数字类型
                elif field.DataType=='Number':
                    test_num=",{0}".format(random.randint(0, 200))
                    unitvalues+=test_num

            unitfields=unitfields[1:]
            unitvalues=unitvalues[1:]
            temp='insert into dbo.{tablename} ({fields}) values ({values})\n go'.format(tablename=self.name,fields=unitfields,values=unitvalues)
            result.append(temp)
        return result

    # 生成sql语句
    def getCreateSql(self,savepath=''):
        unitfield=self.__getFieldCreateSql()
        result="use {db}\nGo\nCreate Table [dbo].[{TableName}](\n\t{Key} int primary key identity(1,1),\t--ID,主键\n{Fields}) ON [PRIMARY]\nGO".format(db=self.db,TableName=self.name,Key=self.key,Fields=unitfield)
        if savepath != "":
            try:
                savedir='{s}'.format(s=savepath)
                if  os.path.exists(savedir) == False:
                    os.makedirs(savedir)
                if savedir[len(savedir)-1] != '/':
                    savedir=savedir+"/"
                savepath='{d}{name}.sql'.format(d=savedir,name=self.name)
                file=open(savepath,'w',encoding='utf-8')
                file.write(result)
                file.close()
                print('输出文件：{s}'.format(s=savepath))
            except Exception as ex:
                print(ex)
        return result
   
    def getaddstrs(self):
        str1='INSERT INTO {0}({1}) VALUES({2});'.format(self.name,'{0}','{1}')
        temp1=''
        temp2=''
        for field in self.fields:
            str=','+field.name
            temp1=temp1+str
            str0=',{0}{1}'.format('{0}',field.name)
            temp2=temp2+str0
        temp1=temp1[1:]
        temp2=temp2[1:]
        str2 = 'INSERT INTO {0}({1}) VALUES({2});'.format(self.name,temp1,temp2)
        return [str1,str2]
    
    def getupdatestrs(self):
        str3='UPDATE {0} SET {1} WHERE {3}={2}{3};'.format(self.name,'{1}','{0}',self.key)
        temp3=''
        for field in self.fields:
            str4=','+field.name+'={0}'+field.name
            temp3=temp3+str4
        temp3=temp3[1:]
        str4='UPDATE {0} SET {1} WHERE {2}={3}{2};'.format(self.name,temp3,self.key,'{0}')
        return str3,str4
    
    def getdeletestr(self):
        result='DELETE FROM {} WHERE 1=1;'.format(self.name)
        return result
    
    def printallstr(self):
        print('---------------------------------------------------------------------------')
        add = self.getaddstrs()
        for i in add:
            print(i)
            print('---------------------------------------------------------------------------')
        update = self.getupdatestrs()
        for i in update:
            print(i)
            print('---------------------------------------------------------------------------')
        print(self.getdeletestr())        
    
    def __getFieldCreateSql(self):
        unitfield=''
        for field in self.fields:
            cn="not null"
            if field.cannull:
                cn=""
            temp="\t{FieldName} {Type} {IsNull}, \t--{remark}\n".format(FieldName=field.name,Type=field.type,IsNull=cn,remark=field.remark)
            unitfield+=temp
        return unitfield

    #生成C#类
    def __getCsharpClass(self):
        unitmember="/// <summary>\n/// {remark}\n/// </summary>\npublic {CsharpType} {FieldName} {gs}\n".format(remark='主键ID',CsharpType='int',FieldName=self.key,gs='{get;set;}')
        for field in self.fields:
            temp="/// <summary>\n/// {remark}\n/// </summary>\npublic {CsharpType} {FieldName} {gs}\n".format(remark=field.remark,CsharpType=field.CsharpType,FieldName=field.name,gs='{get;set;}')
            unitmember+=temp
        return unitmember
    
    def __getCsharpInitor(self):
        result=''
        for f in self.fields:
            if f.cannull:
              continue
            if f.default_val!='':
                if f.DataType=='String':  
                    result+='{fn} = "{dv}";//{rm}\n'.format(fn=f.name,dv=f.default_val,rm=f.remark)
                elif f.DataType=='Number':
                    result+='{fn} = {dv};//{rm}\n'.format(fn=f.name,dv=f.default_val,rm=f.remark)
            elif f.DataType=='String':  
                result+='{fn} = "";//{rm}\n'.format(fn=f.name,rm=f.remark)
            elif f.DataType=='Number':
                result+='{fn} = 0;//{rm}\n'.format(fn=f.name,rm=f.remark)  
        return result

    #创建数据模型类-01Model
    def getCsharpClass(self,savepath=NULL):
        cs='using System;\nusing System.Collections.Generic;\nusing System.Linq;\nusing System.Text;\nusing {db}Upgrade.Models;\nnamespace {db}Upgrade.Models\n{s}\npublic partial class {name}: EntityBase\n{s}\n#region 构造方法\n  /// <summary>\n  /// 初始化实体\n  /// <summary>\npublic {name}(): this(0){s}{e}\n  /// <summary>\n  /// 初始化实体\n  /// <summary>\npublic {name}(int id): base(id){s}{e}\n  #endregion\n{members}{e}\n{e}'.format(db=self.db,name=self.name,members=self.__getCsharpClass(),s="{",e="}")
        if savepath != NULL:
          self.writecs(savepath,'01Models',self.name,cs)
        return cs
    
    #创建数据仓库接口-02IRepository
    def getIRepository(self,savepath=NULL):
        ir='using {db}Upgrade.Models;\nnamespace {db}Upgrade.IRepository{s}\n/// <summary>\n///实体数据仓储接口\n/// <summary>\npublic partial interface I{name}Repository : IBaseRepository<{name}>{s}{e}{e}'.format(db=self.db,name=self.name,s="{",e="}")
        if savepath != NULL:
          self.writecs(savepath,'02IRepository','I{}Repository'.format(self.name),ir)
        return ir

    #创建表数据仓库-03-TableRepository
    def getTableRepository(self,savepath=NULL):        
        tr='using System;\nusing System.Collections.Generic;\nusing System.Linq;\nusing System.Text;\nusing ESIL.DataManager;\nusing {db}Upgrade.IRepository;\nusing {db}Upgrate.Models;\n\nnamespace {db}Upgrade.Repository\n{s}\n    /// <summary>\n    ///实体数据仓储\n    /// <summary>\n    public partial class {name}Repository : BaseRepository<{name}>, I{name}Repository\n    {s}\n        #region 获取格式化SQL语句\n        /// <summary>\n        ///格式化SQL语句\n        /// <summary>\n        /// <param name="type">数据操作类型</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        protected override string FormatSql(DataOperateType type, List<string> fields = null)\n        {s}\n            string strSql = string.Empty;\n            switch (type)\n            {s}\n                case DataOperateType.Add:\n                    {s}\n                        if (DataManager.DBType == DatabaseType.SqlServer)\n                        {s}\n                            if (fields != null && fields.Count > 0)\n                            {s}\n                                var zhanWeiFu = DataManager.ParamPrefix + string.Format(string.Join(",{s}0{e}", fields), new object[] {s} DataManager.ParamPrefix {e});//占位符\n                                strSql = string.Format("{insert1}", new object[] {s} string.Join(",", fields), zhanWeiFu {e});\n                            {e}\n                            else\n                            {s}\n                                strSql = string.Format("{insert2}", new object[] {s} DataManager.ParamPrefix {e});\n                            {e}\n                        {e}\n                    {e}\n                    break;\n                case DataOperateType.Update:\n                    {s}\n                        if (DataManager.DBType == DatabaseType.SqlServer)\n                        {s}\n                            if (fields != null && fields.Count > 0)\n                            {s}\n                                var zhanWeiFu = string.Format(string.Join(",", (from col in fields select col + "={s}0{e}" + col).ToArray()), DataManager.ParamPrefix);\n                                strSql = string.Format("{update1}", new object[] {s} DataManager.ParamPrefix, zhanWeiFu {e});\n                            {e}\n                            else\n                            {s}\n                                strSql = string.Format("{update2}", new object[] {s} DataManager.ParamPrefix {e});\n                            {e}\n                        {e}\n                    {e}\n                    break;\n                case DataOperateType.Delete:\n                    {s}\n                        if (DataManager.DBType == DatabaseType.SqlServer)\n                        {s}\n                            strSql = string.Format("{delete1}");\n                        {e}\n                    {e}\n                    break;\n                default:\n                    throw new Exception("格式化SQL语句没有涉及到的类型：" + type.ToString());\n            {e}\n            return strSql;\n        {e}\n        /// <summary>\n        /// 格式化自增SQL语句\n        /// <summary>\n        protected override string FormatIdentSql()\n        {s}\n            string strSql = string.Format("SELECT IDENT_CURRENT(\'{name}\');");\n            return strSql;\n        {e}\n        #endregion\n        #region 1. 新增单个实体 +Add({name} entity, List<string> fields =null)\n        /// <summary>\n        /// 新增单个实体\n        /// <summary>\n        /// <param name="entity">实体</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int Add({name} entity, List<string> fields = null)\n        {s}\n            if (entity == null) {s} return -1; {e}\n            string strSql = FormatSql(DataOperateType.Add, fields);\n            return DataManager.Execute(strSql, entity);\n        {e}\n        #endregion\n        #region 2. 新增单个实体，返回自增主键 +Add(ref {name} entity, List<string> fields = null)\n        /// <summary>\n        /// 新增单个实体，返回自增主键\n        /// <summary>\n        /// <param name="entity">实体</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int Add(ref {name} entity, List<string> fields = null)\n        {s}\n            int count = Add(entity, fields);\n            if (count > 0)\n            {s}\n                string strSql = FormatIdentSql();\n                entity.{key} = DataManager.ExecuteScalar<int>(strSql);\n                return count;\n            {e}\n            return -1;\n        {e}\n        #endregion\n        #region 3. 新增实体集合 +AddList(IEnumerable<{name}> entities, List<string> fields = null){s}\n        /// <summary>\n        /// 新增实体集合\n        /// <summary>\n        /// <param name="entities">实体集合</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int AddList(IEnumerable<{name}> entities, List<string> fields = null)\n        {s}\n            if (entities == null || entities.Count() <= 0) {s} return -1; {e}\n            string strSql = FormatSql(DataOperateType.Add, fields);\n            return DataManager.Execute(strSql, entities);\n        {e}\n        #endregion\n        #region 4. 编辑单个实体 +Update({name} entity, List<string> fields = null)\n        /// <summary>\n        /// 编辑单个实体\n        /// <summary>\n        /// <param name="entity">实体</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int Update({name} entity, List<string> fields = null)\n        {s}\n            if (entity == null) {s} return -1; {e}\n            string strSql = FormatSql(DataOperateType.Update, fields);\n            return DataManager.Execute(strSql, entity);\n        {e}\n        #endregion\n        #region 5. 编辑实体集合 +UpdateList(IEnumerable<{name}> entities, List<string> fields = null)\n        /// <summary>\n        /// 编辑实体集合\n        /// <summary>\n        /// <param name="entity">实体集合</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int UpdateList(IEnumerable<{name}> entities, List<string> fields = null)\n        {s}\n            if (entities == null || entities.Count() <= 0) {s} return -1; {e}\n            string strSql = FormatSql(DataOperateType.Update, fields);\n            return DataManager.Execute(strSql, entities);\n        {e}\n        #endregion\n        #region 6. 删除单个实体 +Delete(int id)\n        /// <summary>\n        /// 删除单个实体\n        /// <summary>\n        /// <param name="id">主键{key}</param>\n        public override int Delete(int id)\n        {s}\n            string strWhere = string.Empty;\n            strWhere = string.Format("AND {key}={s}0{e} ", new object[] {s} id {e});\n            return DeleteList(strWhere);\n        {e}\n        #endregion\n        #region 7. 删除单个实体 +Delete({name} entity)\n        /// <summary>\n        /// 删除单个实体\n        /// <summary>\n        /// <param name="entity">实体</param>\n        public override int Delete({name} entity)\n        {s}\n            if (entity == null) {s} return -1; {e}\n            return Delete(entity.{key});\n        {e}\n        #endregion\n        #region 8. 删除实体集合 +DeleteList(IEnumerable<int> ids)\n        /// <summary>\n        /// 删除实体集合\n        /// <summary>\n        /// <param name="ids">主键{key}集合</param>\n        public override int DeleteList(IEnumerable<int> ids)\n        {s}\n            if (ids == null || ids.Count() <= 0) {s} return -1; {e}\n            StringBuilder strSql = new StringBuilder();\n            ids.ToList().ForEach(id => {s} strSql.AppendFormat("{s}0{e},", id); {e});\n            strSql = strSql.Remove(strSql.Length - 1, 1);\n            string strWhere = string.Empty;\n            strWhere = string.Format("AND {key} IN ({s}0{e}) ", strSql.ToString());\n            return DeleteList(strWhere);\n        {e}\n        #endregion\n        #region 9. 删除实体集合 +DeleteList(IEnumerable<{name}> entities)\n        /// <summary>\n        /// 删除实体集合\n        /// <summary>\n        /// <param name="entities">实体集合</param>\n        public override int DeleteList(IEnumerable<{name}> entities)\n        {s}\n            if (entities == null || entities.Count() <= 0) {s} return -1; {e}\n            List<int> ids = new List<int>();\n            entities.ToList().ForEach(entity => {s} ids.Add(entity.{key}); {e});\n            return DeleteList(ids);\n        {e}\n        #endregion\n        #region 10. 查询单个实体 +Query(int id)\n        /// <summary>\n        /// 查询单个实体\n        /// <summary>\n        /// <param name="id">主键{key}</param>\n        public override {name} Query(int id)\n        {s}\n            string strWhere = string.Empty;\n            strWhere = string.Format("AND {key}={s}0{e} ", new object[] {s} id {e});\n            return Query(strWhere);\n        {e}\n        #endregion\n    {e}\n{e}'.format(s="{",e="}",db=self.db,name=self.name,key=self.key,insert1=self.getaddstrs()[0],insert2=self.getaddstrs()[1],update1=self.getupdatestrs()[0],update2=self.getupdatestrs()[1],delete1=self.getdeletestr())
        if savepath != NULL:
          self.writecs(savepath,'03Repository','{}Repository'.format(self.name),tr)
        return tr

    #创建视图数据仓库-03-1ViewRepository
    def getViewRepository(self,savepath=NULL):
        vr='using System;\nusing System.Collections.Generic;\nusing System.Linq;\nusing System.Text;\nusing ESIL.DataManager;\nusing {db}Upgrade.Models;\nusing {db}Upgrade.IRepository;\nnamespace {db}Upgrade.Repository\n{s}\n    /// <summary>\n    ///实体数据仓储\n    /// <summary>\n    public partial class {name}Repository : BaseRepository<{name}>, I{name}Repository\n    {s}\n        #region 获取格式化SQL语句\n        /// <summary>\n        ///格式化SQL语句\n        /// <summary>\n        /// <param name="type">数据操作类型</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        protected override string FormatSql(DataOperateType type, List<string> fields = null)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        /// <summary>\n        /// 格式化自增SQL语句\n        /// <summary>\n        protected override string FormatIdentSql()\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 1. 新增单个实体 +Add(T_User entity, List<string> fields = null)\n        /// <summary>\n        /// 新增单个实体\n        /// <summary>\n        /// <param name="entity">实体</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int Add({name} entity, List<string> fields = null)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");        {e}\n        #endregion\n        #region 2. 新增单个实体，返回自增主键 +Add(ref {name} entity, List<string> fields = null)\n        /// <summary>\n        /// 新增单个实体，返回自增主键\n        /// <summary>\n        /// <param name="entity">实体</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int Add(ref {name} entity, List<string> fields = null)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 3. 新增实体集合 +AddList(IEnumerable<{name}> entities, List<string> fields = null)\n        /// <summary>\n        /// 新增实体集合\n        /// <summary>\n        /// <param name="entities">实体集合</param>\n       /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int AddList(IEnumerable<{name}> entities, List<string> fields = null)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");        {e}\n        #endregion\n        #region 4. 编辑单个实体 +Update({name}  entity, List<string> fields = null)\n        /// <summary>\n        /// 编辑单个实体\n        /// <summary>\n        /// <param name="entity">实体</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int Update({name} entity, List<string> fields = null)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");        {e}\n        #endregion\n        #region 5. 编辑实体集合 +UpdateList(IEnumerable<{name}> entities, List<string> fields = null)\n        /// <summary>\n        /// 编辑实体集合\n        /// <summary>\n        /// <param name="entity">实体集合</param>\n        /// <param name="fields">指定的字段，默认为空，给指定字段赋值</param>\n        public override int UpdateList(IEnumerable<{name}> entities, List<string> fields = null)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 6. 删除单个实体 +Delete(int id)\n        /// <summary>\n        /// 删除单个实体\n        /// <summary>\n        /// <param name="id">主键ID</param>\n        public override int Delete(int id)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 7. 删除单个实体 +Delete({name} entity)\n       /// <summary>\n        /// 删除单个实体\n        /// <summary>\n        /// <param name="entity">实体</param>\n        public override int Delete({name} entity)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 8. 删除实体集合 +DeleteList(IEnumerable<int> ids)\n        /// <summary>\n        /// 删除实体集合\n       /// <summary>\n        /// <param name="ids">主键ID集合</param>\n        public override int DeleteList(IEnumerable<int> ids)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 9. 删除实体集合 +DeleteList(IEnumerable<T_User> entities)\n        /// <summary>\n        /// 删除实体集合\n        /// <summary>\n        /// <param name="entities">实体集合</param>\n        public override int DeleteList(IEnumerable<{name}> entities)\n        {s}\n            throw new NotImplementedException("{name}Repository无法实现新增，编辑，删除");\n        {e}\n        #endregion\n        #region 10. 查询单个实体 +Query(int id)\n        /// <summary>\n        /// 查询单个实体\n        /// <summary>\n        /// <param name="id">主键ID</param>\n        public override {name} Query(int id)\n        {s}\n            string strWhere = string.Empty;\n            strWhere = string.Format("AND {key}={s}0{e} ", new object[] {s} id {e});\n            return Query(strWhere);        {e}\n        #endregion\n        #region 11. 查询集体集合 +QueryList(string strWhere = null,List<string> fields = null, string strOrderBy = null, bool isAsc = true, object param = null)\n        /// <summary>\n        /// 查询集体集合\n        /// <summary>\n        /// <param name="strWhere"></param>\n        /// <param name="fields"></param>\n        /// <param name="strOrderBy"></param>\n        /// <param name="isAsc"></param>\n       /// <returns></returns>\n        public override IEnumerable<{name}> QueryList(string strWhere = null, List<string> fields = null, string strOrderBy = null, bool isAsc = true, object param = null)\n        {s}\n            return base.QueryList(strWhere, fields, strOrderBy, isAsc, param);\n        {e}\n        #endregion\n    {e}\n{e}'.format(s="{",e="}",name=self.name,key=self.key)
        if savepath != NULL:
          self.writecs(savepath,'03Repository','{}Repository'.format(self.name),vr)
        return vr

    #创建数据服务接口-04-IService
    def getIService(self,savepath=NULL):
        iS='using System.Collections.Generic;\nusing {db}Upgrade.Models;\nnamespace {db}Upgrade.IService\n{s}\n    /// <summary>\n    /// 实体数据服务接口\n    /// <summary>\n    public partial interface I{name}Service : IBaseService<{name}>\n    {s}\n        #region 拓展接口\n\n        #endregion\n    {e}\n\n{e}'.format(s="{",e="}",db=self.db,name=self.name)
        if savepath != NULL:
          self.writecs(savepath,'04IService','I{}Service'.format(self.name),iS)
        return iS

    #创建数据服务-05-Service
    def getService(self,savepath=NULL):
        s='using System.Collections.Generic;\nusing ESIL.DataManager;\nusing {db}Upgrade.Models;\nusing {db}Upgrade.IService;\nusing {db}Upgrade.Repository;\nusing {db}Upgrade.IRepository;\nnamespace {db}Upgrade.Service\n{s}\n    /// <summary>\n    /// 实体数据服务\n    /// <summary>\n    public partial class {name}Service : BaseService<{name}>, I{name}Service\n    {s}\n        /// <summary>\n        /// 创建数据仓储\n        /// <summary>\n        protected override void CreateRepository()\n        {s}\n            Repository = RepositoryFactory.CreateRepository<I{name}Repository, {name}Repository>();\n        {e}\n        #region 拓展接口\n        #endregion\n    {e}\n{e}'.format(s="{",e="}",name=self.name)
        if savepath != NULL:
          self.writecs(savepath,'05Service','{}Service'.format(self.name),s)
        return s

    #获取字段列表
    def getFiledList(self):
        totalf=''
        for f in self.fields:
            totalf+=',"{}"'.format(f.name)
        totalf=totalf[1:]
        result='new List<string>(){s}{fs}{e};'.format(s="{",e="}",fs=totalf)
        return result

    def writecs(self,savepath,dir,name,txt):
                savedir='{s}/{dir}'.format(s=savepath,dir=dir)
                if  os.path.exists(savedir) == False:
                    os.makedirs(savedir)
                savepath='{d}/{name}.cs'.format(d=savedir,name=name)
                file=open(savepath,'w',encoding='utf-8')
                file.write(txt)
                file.close()
                print('输出文件：{s}'.format(s=savepath))


