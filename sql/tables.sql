-- ----------------------------
-- Table structure for kuking_category
-- ----------------------------
CREATE TABLE IF NOT EXISTS kuking_category (
  id_category bigint  NOT NULL,
  category_name varchar(45) NOT NULL,
  PRIMARY KEY  (id_category)
) ;

-- ----------------------------
-- Table structure for kuking_recepts
-- ----------------------------
CREATE TABLE IF NOT EXISTS kuking_recepts (
  id_recepts bigint  NOT NULL,
  recept_category bigint NOT NULL,
  podcategory varchar(100) default 'разное',
  recept_name varchar(100) NOT NULL,
  recept_sostav text,
  recept_instuction text NOT NULL,
  PRIMARY KEY  (id_recepts)
) ;