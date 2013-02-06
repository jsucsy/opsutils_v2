'''
Created on Jan 24, 2013

@author: JSU
'''

import ListFileNames as lfn
import xml.etree.ElementTree as etree

   
def extract_all_fields(source, fund, carvemap):
    '''get all relevant fields from report, return as list'''
    results = {}
    
    tree = etree.parse(source)
    root = tree.getroot()
    #print "root len: %s" % len(root)
    print root.tag
    
    for group_header in root.iter("%sGroup_Header" % EXPORT_HEADER):
        print group_header
#        for key in carvemap.iterkeys():
#            print key
        results['FirstPeriodToDate'] = float(group_header.attrib['FirstPeriodToDate']) + carvemap[fund][0]
        results['LastPeriodToDate'] = float(group_header.attrib['LastPeriodToDate']) + carvemap[fund][0]
        
    for subheader in root.iter("%sGroup4" % EXPORT_HEADER):
        levelsum = 0
        for table in subheader.iter("%sTable1Detail" % EXPORT_HEADER):
            levelsum += float(table.attrib['PeriodToDate'])
        #print "%s : %s" % (subheader.attrib['Detail'], levelsum)
        results[subheader.attrib['Detail']] = levelsum

    print results
    return results

def list_funds(source):
    '''get a list of all fund names for report filenames from map file'''
    fundmap = {}
    for line in open(source, 'rb+'):        
        fields = line.split('|')
        fundmap[fields[0]] = fields[1]
        
    return fundmap

def get_carveout(source):
    '''return dict; key = fund, value = 3 vals in list: [Total, Management Fee, Performance Fee]'''
    carveout_map = {}
    
    for line in open(source, 'rb+'):
        mgmt = 0
        perf = 0
        fields = line.split('|')
        if fields[1] != "CARVE": 
            mgmt = float(fields[1])
        if fields[2] != "CARVE": 
            perf = float(fields[2])
        carveout_map[fields[0]] = [mgmt+perf, fields[1], fields[2]]
#    for fund in carveout_map.iterkeys():
#        print "%s|%s" % (fund, carveout_map[fund])
    return carveout_map
        
        
def get_categories(source_map, source_list):
    '''remap Geneva report categories to preferred categories for report'''
    cat_map = {}
    final_map = []
    for line in open(source_map, 'rb+'):
        fields = line.split('|')
        cat_map[fields[0]] = fields[1]
        
    for line in open(source_list, 'rb+'):
        final_map.append(line.split('|')[0])
        
    return cat_map, final_map
        

if __name__ == '__main__':
    
    #SOURCEDIR = "C:\\Users\\JSU\\AppData\\Local\\Temp\\"
    #SOURCEDIR = "C:\\Users\\josh\\Dropbox\\Work\\MonthEndRebal\\"
    #SOURCEFILE = "Report Statement of Changes in Net Assets - %s.xml"
    
    EXPORT_HEADER = "{Statement_x0020_of_x0020_Changes_x0020_in_x0020_Net_x0020_Assets}"
    SOURCEDIR = "C:\\Ops\\Geneva\\DailyNAV\\20130201\\"
    REFDIR = "C:\\Ops\\Geneva\\DailyNAV\\Ref\\"
    SOURCEFILE = "Report Statement of Changes in Net Assets - %s.xml"
    OUTFILE = "%s_output.txt" % SOURCEDIR
    CARVEFILE = "%sfee_adj.txt" % REFDIR
    CATMAPFILE = "%scategory_map.txt" % REFDIR
    CATLISTFILE = "%sfinal_cat_list.txt" % REFDIR
    
    
    #lfn.list_names(SOURCEDIR)
    FUNDMAP = list_funds("%sfund_map.txt" % REFDIR)
    CARVEMAP = get_carveout(CARVEFILE)
    CATMAP, CATFINAL = get_categories(CATMAPFILE, CATLISTFILE)
    
    RAW_RESULTS = {}
    CATFINAL.insert(0,"Fund")
    
    
    with open(OUTFILE, 'wb+') as out:
    
        out.write("%s\n" % "|".join(CATFINAL))
            
        for fund in FUNDMAP.iterkeys():
            results = extract_all_fields("%s%s" % (SOURCEDIR,SOURCEFILE % fund), fund, CARVEMAP)
            RAW_RESULTS[fund] = results
            
        for fund in RAW_RESULTS.iterkeys():
            fund_results = [0]*len(CATFINAL)
            fund_results[0] = FUNDMAP[fund]
            for result in RAW_RESULTS[fund].iterkeys():
                fund_results[CATFINAL.index(CATMAP[result])] += RAW_RESULTS[fund][result]
                
            out.write("%s\n" % "|".join(map(str,fund_results)))
            
#        for fund in RAW_RESULTS.iterkeys():
#            for result in RAW_RESULTS[fund].iterkeys():
#                if result not in HEADERMAP:
#                    HEADERMAP.append(result)
                    
#        for fund in RAW_RESULTS.iterkeys():
#            fund_results = [""]*len(HEADERMAP)
#            fund_results[0] = fund
#            for result in RAW_RESULTS[fund].iterkeys():
#                fund_results[HEADERMAP.index(result)] = "%s" % RAW_RESULTS[fund][result]
#            out.write("%s\n" % "|".join(fund_results))
            
            
            
            
            
#        for header in HEADERMAP:
#            print header
            
#        out.write("%s\n" % ("|".join(HEADERMAP)))    
#            fund_results = [""]*len(HEADERMAP)
#            fund_results[0] = fund
#            for k in results:
#                #print HEADERMAP.index(k)
#                fund_results[HEADERMAP.index(k)] = "%s" % results[k]
#                #out.write("%s : %s | " % (k,results[k]))
#            out.write("%s\n" % "|".join(fund_results))
#            
        
    
        
        
        
#**************unused code***********************


#def list_headers(source):
#    header_map = []
#    header_map.append("FundName")
#    for line in open(source, 'rb+'):
#        header_map.append(line.split('|')[0])
#        
#    return header_map

#    table1 = root.findall("{Statement_x0020_of_x0020_Changes_x0020_in_x0020_Net_x0020_Assets}Table1")
#    grp_hdr_collection = table1.findall("{Statement_x0020_of_x0020_Changes_x0020_in_x0020_Net_x0020_Assets}Group_Header_Collection")
#    
    #root = tree.getiterator()
    
#    for child in root:
#        print child.tag, child.attrib
    #print root[0][0][0][0].text

#def walk_tree_test(source):
#    '''walk xml tree for all relevant information for rebal'''
#    tree = etree.parse(source)
#    root = tree.getroot()
#    total_tree = walk_it_all(root)
#    print len(total_tree)
#    print total_tree[0]
##    print root.findall('{"Change in Unrealized FX Gain/Loss"}Detail')
##    print tree.findall('.//')
#    
#    
#def walk_it_all(level):
#    '''walk all xml levels, return list of lists with full element at each level'''
#    vals_at_level = []
#    for child in level:
#        #print child
#        vals_at_level.append(walk_it_all(child))
#    
#    return vals_at_level
#
#        
