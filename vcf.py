def update_info_tags(i_tags,tool_name):
    i_tags = i_tags.strip(";calledBy="+tool_name)
    i_tags = i_tags.replace(";",";"+tool_name+"_")
    i_tags = tool_name+"_"+i_tags
    return i_tags
def update_fmt_tags(f_tags,tool_name):
    f_tags = f_tags.replace(":",":"+tool_name+"_")
    f_tags = tool_name+"_"+f_tags
    return f_tags

class vcf:
    def __init__(self,file_loc: str,tool_name: str):
        self.file_loc = file_loc
        self.tool_name = tool_name
        info = {}
        fmt = {}
        fmt_data = {}
        base_data = {}
        header = []
        with open(file_loc,"r") as tmp:
            for line in tmp:
                if line.startswith("#"):
                    header.append(line)
                    continue
                var_data = line.split("\t")
                ukey = var_data[0]+"|"+var_data[1]+":"+var_data[3]+">"+var_data[4]
                info[ukey] = var_data[7]+";calledBy="+tool_name
                fmt[ukey] = var_data[8]        ##
                fmt_data[ukey] = var_data[9]   ##
                base_data[ukey] = var_data[0]+"\t"+var_data[1]+"\t"+var_data[2]+"\t"+var_data[3]+"\t"+var_data[4]+"\t"+var_data[5]+"\t"+var_data[6]
        self.info= info
        self.fmt= fmt
        self.fmt_data= fmt_data
        self.base_data = base_data
        self.vcf_header = ''.join(header)      ##
    def merge_vcf(self,vcf2):
        for k in vcf2.info:
            if k in self.info:
                v_data = update_info_tags(self.info[k],self.tool_name)
                v2_data = update_info_tags(vcf2.info[k],vcf2.tool_name)
                self.info[k] = v_data+";"+v2_data+";calledBy="+self.tool_name+"+"+vcf2.tool_name
                self.fmt[k] = update_fmt_tags(self.fmt[k],self.tool_name)+";"+update_fmt_tags(vcf2.fmt[k],vcf2.tool_name)
                self.fmt_data[k] = self.fmt_data[k].strip("\n")+";"+vcf2.fmt_data[k]
            else:
                self.base_data[k] = vcf2.base_data[k]
                self.info[k] =  vcf2.info[k]
                self.fmt[k] =  vcf2.fmt[k]
                self.fmt_data[k] =  vcf2.fmt_data[k]
    def flaten_vcf(self):
        flat_data = []
        flat_data.append(self.vcf_header)
        for k in self.base_data:
            line = self.base_data[k]+"\t"+self.info[k]+"\t"+self.fmt[k]+"\t"+self.fmt_data[k]
            flat_data.append(line)
        return ''.join(flat_data)

#read and merge the new vcf file with merge_vcf() method and use first vcf as reference
abc = vcf("freebayes_raw.vcf","FreeBayes")
bcd = vcf("varscan_raw.vcf","Varscan")
abc.merge_vcf(bcd)
#write out the vcf file
with open("merged_data.vcf","w") as mo:
    mo.write(abc.flaten_vcf())