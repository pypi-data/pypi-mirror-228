#ifndef CUBAO_NAIVE_SVG_HPP
#define CUBAO_NAIVE_SVG_HPP

// upstream
// https://github.com/cubao/headers/tree/main/include/cubao/naive_svg.hpp
// migrated from https://github.com/cubao/naive-svg/blob/master/svg.hpp

#include <vector>
#include <map>
#include <string>

#include <fstream>
#include <ostream>
#include <sstream>

namespace cubao
{
// https://en.wikipedia.org/wiki/Fluent_interface
// https://rapidjson.org/md_doc_tutorial.html
// https://www.tutorialspoint.com/what-is-function-chaining-in-javascript
#ifndef SETUP_FLUENT_API
#define SETUP_FLUENT_API(Klass, VarType, VarName)                              \
    Klass &VarName(const VarType &v)                                           \
    {                                                                          \
        VarName##_ = v;                                                        \
        return *this;                                                          \
    }                                                                          \
    VarType &VarName() { return VarName##_; }                                  \
    const VarType &VarName() const { return VarName##_; }
#endif

#ifndef SETUP_FLUENT_API_FOR_SVG_ELEMENT
#define SETUP_FLUENT_API_FOR_SVG_ELEMENT(KlassType)                            \
    SETUP_FLUENT_API(KlassType, Color, stroke)                                 \
    SETUP_FLUENT_API(KlassType, Color, fill)                                   \
    SETUP_FLUENT_API(KlassType, double, stroke_width)
#endif

struct SVG
{
    using PointType = std::array<double, 2>;
    enum COLOR
    {
        RED = 0xFF0000,
        GREEN = 0x00FF00, // not css green
        BLUE = 0x0000FF,
        YELLOW = 0xFFFF00,
        WHITE = 0xFFFFFF,
        GRAY = 0x9B9B9B,
        BLACK = 0x000000,
        NONE = -1,
    };

    struct Color
    {
        Color(int rgb = -1 /* NONE */)
        {
            if (rgb >= 0) {
                r_ = (rgb >> 16) & 0xFF;
                g_ = (rgb >> 8) & 0xFF;
                b_ = rgb & 0xFF;
            }
        }
        Color(int r, int g, int b, float a = -1.f) : r_(r), g_(g), b_(b), a_(a)
        {
        }
        SETUP_FLUENT_API(Color, int, r)
        SETUP_FLUENT_API(Color, int, g)
        SETUP_FLUENT_API(Color, int, b)
        SETUP_FLUENT_API(Color, float, a)
        bool invalid() const
        {
            return r_ < 0 || g_ < 0 || b_ < 0 || //
                   r_ > 255 || g_ > 255 || b_ > 255;
        }

        friend std::ostream &operator<<(std::ostream &out, const SVG::Color &c);
        void write(std::ostream &out) const
        {
            if (invalid()) {
                out << "none";
                return;
            }
            if (0.f <= a_ && a_ <= 1.f) {
                out << "rgba(" << r_ << "," << g_ << "," << b_ << "," << a_
                    << ")";
            } else {
                out << "rgb(" << r_ << "," << g_ << "," << b_ << ")";
            }
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

      private:
        int r_{-1}, g_{-1}, b_{-1};
        float a_{-1.f};
    };

    enum ELEMENT
    {
        POLYLINE,
        POLYGON,
        CIRCLE,
        TEXT
    };

    struct Element
    {
        void fit_into(double xmin, double xmax, double ymin, double ymax, //
                      double width, double height)
        {
            // fit bbox[xmin:xmax, ymin:ymax] into viewBox[0:width, 0:height]
            double xspan = xmax - xmin;
            double yspan = ymax - ymin;
            for (auto &pt : points_) {
                pt[0] = (pt[0] - xmin) / xspan * width;
                pt[1] = (pt[1] - ymin) / yspan * height;
            }
        }

      protected:
        std::vector<PointType> points_;
        Color stroke_{COLOR::BLACK};
        double stroke_width_{1.0};
        Color fill_{COLOR::NONE};
    };

    struct Polyline : Element
    {
        Polyline(const std::vector<PointType> &points) { points_ = points; }
        SETUP_FLUENT_API(Polyline, std::vector<SVG::PointType>, points)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Polyline)

        friend std::ostream &operator<<(std::ostream &out,
                                        const SVG::Polyline &e);
        void write(std::ostream &out) const
        {
            out << "<polyline";
            out << " style='stroke:" << stroke_      //
                << ";stroke-width:" << stroke_width_ //
                << ";fill:" << fill_                 //
                << "'";
            out << " points='";
            for (auto &pt : points_) {
                out << pt[0] << "," << pt[1] << " ";
            }
            out << "'";
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }
    };

    struct Polygon : Element
    {
        Polygon(const std::vector<PointType> &points) { points_ = points; }
        SETUP_FLUENT_API(Polygon, std::vector<SVG::PointType>, points)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Polygon)

        friend std::ostream &operator<<(std::ostream &out, const Polygon &e);
        void write(std::ostream &out) const
        {
            out << "<polygon";
            out << " style='stroke:" << stroke_      //
                << ";stroke-width:" << stroke_width_ //
                << ";fill:" << fill_                 //
                << "'";
            out << " points='";
            for (auto &pt : points_) {
                out << pt[0] << "," << pt[1] << " ";
            }
            out << "'";
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }
    };

    struct Circle : Element
    {
        Circle(const PointType &center, double r = 1.0)
        {
            points_ = {center};
            r_ = r;
        }
        Circle &center(const PointType &center)
        {
            points_[0] = center;
            return *this;
        }
        PointType &center() { return points_[0]; }
        const PointType &center() const { return points_[0]; }
        Circle &x(double x)
        {
            points_[0][0] = x;
            return *this;
        }
        double &x() { return points_[0][0]; }
        const double &x() const { return points_[0][0]; }
        Circle &y(double y)
        {
            points_[0][0] = y;
            return *this;
        }
        double &y() { return points_[0][0]; }
        const double &y() const { return points_[0][0]; }

        SETUP_FLUENT_API(Circle, double, r)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Circle)

        friend std::ostream &operator<<(std::ostream &out,
                                        const SVG::Circle &e);
        void write(std::ostream &out) const
        {
            out << "<circle r='" << r_ << "'"               //
                << " cx='" << x() << "' cy='" << y() << "'" //
                << " style='stroke:" << stroke_             //
                << ";stroke-width:" << stroke_width_        //
                << ";fill:" << fill_ << "'"                 //
                << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

      protected:
        double r_{1.0};
    };

    struct Text : Element
    {
        Text(const PointType &p, const std::string &text, int fontsize = 10.0)
        {
            points_ = {p};
            text_ = text;
            fontsize_ = fontsize;
            fill_ = COLOR::BLACK;
        }
        Text &position(const PointType &p)
        {
            points_[0] = p;
            return *this;
        }
        PointType &position() { return points_[0]; }
        const PointType &position() const { return points_[0]; }

        Text &x(double x)
        {
            points_[0][0] = x;
            return *this;
        }
        double &x() { return points_[0][0]; }
        const double &x() const { return points_[0][0]; }
        Text &y(double y)
        {
            points_[0][0] = y;
            return *this;
        }
        double &y() { return points_[0][0]; }
        const double &y() const { return points_[0][0]; }

        SETUP_FLUENT_API(Text, std::string, text)
        SETUP_FLUENT_API(Text, std::vector<std::string>, lines)
        SETUP_FLUENT_API(Text, double, fontsize)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Text)

        //         // text-anchor="start"
        //    <style>
        // * {
        //     stroke-width: 5px;
        // }
        // text {
        //     font-size: 20px;
        // }
        //     </style>

        friend std::ostream &operator<<(std::ostream &out, const SVG::Text &e);

        void write(std::ostream &out) const
        {
            out << "<text"                                //
                << " x='" << x() << "' y='" << y() << "'" //
                << " fill='" << fill_ << "'"              //
                << " font-size='" << fontsize_ << "'"     //
                << " font-family='monospace'"             //
                << ">" << html_escape(text_);
            if (!lines_.empty()) {
                double fontsize = fontsize_ / 5.0;
                for (auto &line : lines_) {
                    out << "<tspan xml:space='preserve' x='" << x() //
                        << "' dy='" << fontsize                     //
                        << "' fill='" << fill_                      //
                        << "' font-size='" << fontsize              //
                        << "' font-family='monospace'>"             //
                        << html_escape(line) << "</tspan>";
                }
            }
            out << "</text>";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        static std::string html_escape(const std::string &text)
        {
            const static std::vector<std::string> escapes = {
                "&amp;", "&quot;", "&apos;", "&lt;", "&gt;"};
            std::map<int, int> replace;
            for (size_t pos = 0; pos != text.size(); ++pos) {
                const char c = text[pos];
                if (c == '&') {
                    replace[pos] = 0;
                } else if (c == '\"') {
                    replace[pos] = 1;
                } else if (c == '\'') {
                    replace[pos] = 2;
                } else if (c == '<') {
                    replace[pos] = 3;
                } else if (c == '>') {
                    replace[pos] = 4;
                }
            }
            if (replace.empty()) {
                return text;
            }
            std::string buffer;
            buffer.reserve(text.size() + 6 * replace.size());
            // TODO
            for (size_t pos = 0; pos != text.size(); ++pos) {
                auto itr = replace.find(text[pos]);
                if (itr == replace.end()) {
                    buffer.append(&text[pos], 1);
                } else {
                    buffer.append(escapes[itr->second]);
                }
            }
            return buffer;
        }

      protected:
        std::string text_;
        std::vector<std::string> lines_;
        double fontsize_{10.0};
    };

    SVG(double width, double height) : width_(width), height_(height) {}
    ~SVG()
    {
        for (auto &pair : elements_) {
            const auto type = pair.first;
            if (type == ELEMENT::POLYGON) {
                delete (Polygon *)pair.second;
            } else if (type == ELEMENT::POLYLINE) {
                delete (Polyline *)pair.second;
            } else if (type == ELEMENT::CIRCLE) {
                delete (Circle *)pair.second;
            } else if (type == ELEMENT::TEXT) {
                delete (Text *)pair.second;
            }
        }
    }

    SVG clone() const {}

    SETUP_FLUENT_API(SVG, double, width)
    SETUP_FLUENT_API(SVG, double, height)
    SETUP_FLUENT_API(SVG, double, grid_step)
    SETUP_FLUENT_API(SVG, std::vector<double>, grid_x)
    SETUP_FLUENT_API(SVG, std::vector<double>, grid_y)
    SETUP_FLUENT_API(SVG, Color, grid_color)
    SETUP_FLUENT_API(SVG, Color, background)

    Polygon &add_polygon(const std::vector<PointType> &points)
    {
        auto ptr = new Polygon(points);
        elements_.push_back({ELEMENT::POLYGON, (void *)ptr});
        return *ptr;
    }

    Polyline &add_polyline(const std::vector<PointType> &points)
    {
        auto ptr = new Polyline(points);
        elements_.push_back({ELEMENT::POLYLINE, (void *)ptr});
        return *ptr;
    }

    Circle &add_circle(const PointType &center, double r = 1.0)
    {
        auto ptr = new Circle(center, r);
        elements_.push_back({ELEMENT::CIRCLE, (void *)ptr});
        return *ptr;
    }

    Text &add_text(const PointType &position, const std::string &text,
                   int fontsize = 10.0)
    {
        auto ptr = new Text(position, text, fontsize);
        elements_.push_back({ELEMENT::TEXT, (void *)ptr});
        return *ptr;
    }

    void write(std::ostream &out) const
    {
        out << "<svg width='" << width_ << "' height='" << height_ << "'"
            << " xmlns='http://www.w3.org/2000/svg' "
               "xmlns:xlink='http://www.w3.org/1999/xlink'>";
        if (!background_.invalid()) {
            out << "\n\t<rect width='100%' height='100%' fill='" //
                << background_                                   //
                << "'/>";
        }
        double xmin = 0.0, xmax = width_, xstep = grid_step_;
        double ymin = 0.0, ymax = height_, ystep = grid_step_;
        if (grid_x_.size() == 3 && grid_y_.size() == 3) {
            xmin = grid_x_[0];
            xmax = grid_x_[1];
            xstep = grid_x_[2];
            ymin = grid_y_[0];
            ymax = grid_y_[1];
            ystep = grid_y_[2];
        }
        if (xstep > 0 && ystep > 0 && xmin < xmax && ymin < ymax) {
            SVG::Color grid_color = SVG::COLOR::GRAY;
            if (!grid_color_.invalid()) {
                grid_color = grid_color_;
            }
            for (double x = xmin; x < xmax; x += xstep) {
                out << "\n\t"
                    << SVG::Polyline({{x, ymin}, {x, ymax}}).stroke(grid_color);
            }
            for (double y = ymin; y < ymax; y += ystep) {
                out << "\n\t"
                    << SVG::Polyline({{xmin, y}, {xmax, y}}).stroke(grid_color);
            }
        }
        for (auto &pair : elements_) {
            out << "\n\t";
            if (pair.first == ELEMENT::POLYGON) {
                ((Polygon *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::POLYLINE) {
                ((Polyline *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::CIRCLE) {
                ((Circle *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::TEXT) {
                ((Text *)pair.second)->write(out);
            }
        }
        out << "\n</svg>";
    }

    void save(std::string path) const
    {
        std::ofstream file(path);
        write(file);
        file.close();
    }

    void fit_to_bbox(double xmin, double xmax, double ymin, double ymax)
    {
        for (auto &pair : elements_) {
            ((Element *)pair.second)
                ->fit_into(xmin, ymax, ymin, ymax, width_, height_);
        }
    }

  private:
    // size
    double width_, height_;
    // grid
    double grid_step_{-1.0};
    std::vector<double> grid_x_, grid_y_; // low, high, step
    Color grid_color_{COLOR::GRAY};
    // background
    Color background_{COLOR::NONE};
    // elements
    std::vector<std::pair<ELEMENT, void *>> elements_;
};

inline std::ostream &operator<<(std::ostream &out, const SVG::Color &c)
{
    c.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Polyline &p)
{
    p.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Polygon &p)
{
    p.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Circle &c)
{
    c.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Text &t)
{
    t.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG &s)
{
    s.write(out);
    return out;
}

} // namespace cubao

#undef SETUP_FLUENT_API
#undef SETUP_FLUENT_API_FOR_SVG_ELEMENT

#endif
