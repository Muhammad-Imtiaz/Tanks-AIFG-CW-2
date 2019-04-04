VERTEX_SHADER = """
#version 330
uniform mat4 Projection;

// per vertex
in vec2 in_vert;
in vec2 in_texture;

// per instance
in vec2 in_pos;
in float in_angle;
in vec2 in_scale;
in vec4 in_sub_tex_coords;
in vec4 in_color;
in vec3 in_light;

out vec2 v_texture;
out vec4 v_color;
out vec2 v_pos;
out vec3 v_light;

void main() {
    mat2 rotate = mat2(
                cos(in_angle), sin(in_angle),
                -sin(in_angle), cos(in_angle)
            );
    vec2 pos;
    v_pos = in_pos + vec2(rotate * (in_vert * in_scale));
    gl_Position = Projection * vec4(v_pos, 0.0, 1.0);

    vec2 tex_offset = in_sub_tex_coords.xy;
    vec2 tex_size = in_sub_tex_coords.zw;

    v_texture = (in_texture * tex_size + tex_offset) * vec2(1, -1);
    v_color = in_color;
    v_light = vec3(in_light[0], in_light[1], in_light[2]);
}
"""

FRAGMENT_SHADER = """
#version 330
uniform sampler2D Texture;

in vec2 v_texture;
in vec4 v_color;

out vec4 f_color;

void main() {
    vec4 basecolor = texture(Texture, v_texture);
    basecolor = basecolor * v_color;
    if (basecolor.a == 0.0){
        discard;
    }
    f_color = basecolor;
}
"""

FRAGMENT_SHADER_LIGHT = """
#version 330
uniform sampler2D Texture;
uniform int point_light_count;
uniform vec2 point_light;

in vec2 v_texture;
in vec4 v_color;
in vec2 v_pos;
in vec3 v_light;

out vec4 f_color;

float ambient = 0.1;

void main() {
    vec4 basecolor = texture(Texture, v_texture);

    basecolor = basecolor * v_color;
    if (basecolor.a == 0.0){
        discard;
    }
    f_color = basecolor * (0, 0, 0, 1);

    float d = distance(v_pos, point_light);

    if (d < 200) {
      ambient = 1 - (d / 200);
    }
    if (ambient < 0.1) {
        ambient = 0.1;
    }


    f_color.r = basecolor.r * ambient;
    f_color.b = basecolor.b * ambient;
    f_color.g = basecolor.g * ambient;

}
"""