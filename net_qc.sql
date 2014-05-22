-- phpMyAdmin SQL Dump
-- version 3.5.8.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2014 年 03 月 04 日 14:58
-- 服务器版本: 5.5.32-0ubuntu0.13.04.1
-- PHP 版本: 5.4.9-4ubuntu2.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `net_qc`
--

-- --------------------------------------------------------

--
-- 表的结构 `category`
--

CREATE TABLE IF NOT EXISTS `category` (
  `parentid` smallint(5) unsigned zerofill NOT NULL COMMENT '父级菜单编号，顶级菜单的父级菜单编号为0',
  `catid` smallint(6) NOT NULL,
  `catname` varchar(255) NOT NULL,
  PRIMARY KEY (`parentid`,`catname`),
  KEY `catid` (`catid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `category`
--

INSERT INTO `category` (`parentid`, `catid`, `catname`) VALUES
(00000, 0, '通知公告'),
(00000, 1, '课程介绍'),
(00001, 1, '课程概况'),
(00002, 1, 'PPT'),
(00000, 2, '教学资源');

-- --------------------------------------------------------

--
-- 表的结构 `entries`
--

CREATE TABLE IF NOT EXISTS `entries` (
  `entry_id` int(255) NOT NULL AUTO_INCREMENT,
  `parent_id` smallint(255) NOT NULL,
  `cat_id` smallint(4) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text,
  `author` smallint(255) NOT NULL,
  `post_time` datetime NOT NULL,
  `click_rates` int(255) unsigned zerofill NOT NULL,
  PRIMARY KEY (`entry_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- 转存表中的数据 `entries`
--

INSERT INTO `entries` (`entry_id`, `parent_id`, `cat_id`, `title`, `content`, `author`, `post_time`, `click_rates`) VALUES
(2, 0, 0, '放假通知', '放假通知', 1, '2014-02-22 10:18:01', 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
(3, 0, 0, '考试通知', '考试通知', 1, '2014-02-04 10:18:43', 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
(4, 0, 0, '修改考试时间', '修改', 1, '2014-02-10 10:19:20', 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
(6, 1, 1, '后勤服务中心班子慰问春节在岗职工', '喜迎新春之际，合家团圆之时，为保一方平安，总有人“舍小家，顾大家”坚守在工作岗位，1月30日癸巳蛇年除夕上午，后勤服务中心班子成员走访慰问了学生餐厅、学生公寓、楼宇值班室、校园物业、水电暖值班室的工作人员，向节日期间仍然坚守岗位的一线劳动者表示衷心感谢，同时也向他们及家人致以亲切慰问和新年的祝福。2\r\n每到一处，班子成员都和大家深入交谈，详细了解各部门安全生产情况和节日期间值班人员安排情况。在学生餐厅和公寓，班子成员详细询问了留校过年学生们的聚餐准备情况和生活情况，叮嘱工作人员要一如既往的为学生们做好服务工作，让学生感受到家的温暖。在校园物业值班室，班子成员指出，逢年过节，你们最辛苦，虽然今年燃放烟花爆竹的可能会少些，但是大家的工作量依然会很大，希望大家要学习习近平总书记看望北京环卫工人时的讲话精神，发扬时传祥“宁愿一人脏，换来万家净”精神，保证校园的干净整洁。在水、电、暖值班室，班子成员指出，大家岗位平凡，但责任重大，节日期间大家要认真坚守岗位，确保正常运转，对出现的报修情况要及时响应、尽快排查、迅速修复，保证在校师生过一个平安、祥和的春节。', 1, '2014-02-27 00:00:00', 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000);

-- --------------------------------------------------------

--
-- 表的结构 `friends_link`
--

CREATE TABLE IF NOT EXISTS `friends_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `friends_link`
--

INSERT INTO `friends_link` (`id`, `title`, `link`) VALUES
(1, '哈尔滨工业大学', 'http://www.hit.edu.cn'),
(2, 'Google', 'http://www.google.com');

-- --------------------------------------------------------

--
-- 表的结构 `teachers`
--

CREATE TABLE IF NOT EXISTS `teachers` (
  `id` smallint(255) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `job` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `teachers`
--

INSERT INTO `teachers` (`id`, `name`, `job`) VALUES
(1, 'Bill', '教授'),
(2, 'Gates', '教授');

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `pwd` varchar(255) NOT NULL,
  `authority` tinyint(255) NOT NULL COMMENT '0为管理员，1为教师，2为学生',
  `regdate` datetime NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`uid`, `name`, `pwd`, `authority`, `regdate`) VALUES
(1, 'admin', '123456qwe', 0, '2014-02-22 09:39:30');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
